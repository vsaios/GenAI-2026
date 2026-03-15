"""Report CRUD endpoints with optional 311 email and image upload."""
import os
import sys
import uuid
import shutil
from typing import List, Optional
from pathlib import Path

import httpx
from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import ReportModel

# Wire up AI path so we can import email_sender
_here = os.path.dirname(os.path.abspath(__file__))
AI_PATH = os.path.normpath(os.path.join(_here, "..", "..", "..", "ai", "Moorcheh"))
if AI_PATH not in sys.path:
    sys.path.insert(0, AI_PATH)

try:
    from email_sender import send_pothole_report
    EMAIL_AVAILABLE = True
except Exception:
    EMAIL_AVAILABLE = False

router = APIRouter(prefix="/reports", tags=["reports"])

GEOAPIFY_KEY = os.environ.get("GEOAPIFY_API_KEY", "")
UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class ReportResponse(BaseModel):
    id: str
    latitude: float
    longitude: float
    issue_type: str
    severity: str
    timestamp: str
    status: str
    image_path: Optional[str] = None
    email_status: Optional[str] = None

    class Config:
        from_attributes = True


def _to_iso_utc(dt):
    s = dt.isoformat()
    if dt.tzinfo is None and "Z" not in s and "+" not in s:
        s += "Z"
    return s


def _reverse_geocode(lat: float, lng: float) -> str:
    """Use Geoapify to convert lat/lng to a street address."""
    if not GEOAPIFY_KEY:
        return f"{lat:.6f}, {lng:.6f}"
    try:
        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lng}&apiKey={GEOAPIFY_KEY}"
        resp = httpx.get(url, timeout=5)
        data = resp.json()
        props = data.get("features", [{}])[0].get("properties", {})
        street = props.get("street", "")
        city = props.get("city", "Toronto")
        return f"{street}, {city}" if street else props.get("formatted", f"{lat:.6f}, {lng:.6f}")
    except Exception:
        return f"{lat:.6f}, {lng:.6f}"


@router.get("", response_model=List[ReportResponse])
def list_reports(db: Session = Depends(get_db)):
    rows = db.query(ReportModel).order_by(ReportModel.timestamp.desc()).all()
    return [
        ReportResponse(
            id=r.id,
            latitude=r.latitude,
            longitude=r.longitude,
            issue_type=r.issue_type,
            severity=r.severity,
            timestamp=_to_iso_utc(r.timestamp),
            status=r.status,
            image_path=r.image_path,
        )
        for r in rows
    ]


@router.post("", response_model=ReportResponse)
async def create_report(
    latitude: float = Form(...),
    longitude: float = Form(...),
    issue_type: str = Form(...),
    severity: str = Form(...),
    send_email: bool = Form(False),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    report_id = str(uuid.uuid4())

    # Save image if provided
    image_path = None
    if image and image.filename:
        ext = Path(image.filename).suffix or ".jpg"
        filename = f"{report_id}{ext}"
        dest = UPLOAD_DIR / filename
        with open(dest, "wb") as f:
            shutil.copyfileobj(image.file, f)
        image_path = f"/uploads/{filename}"

    report = ReportModel(
        id=report_id,
        latitude=latitude,
        longitude=longitude,
        issue_type=issue_type,
        severity=severity,
        status="open",
        image_path=image_path,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    ts = _to_iso_utc(report.timestamp)

    # Send 311 email if requested
    email_status = None
    if send_email and EMAIL_AVAILABLE:
        road = _reverse_geocode(latitude, longitude)
        image_abs_path = None
        if image_path:
            image_abs_path = str(UPLOAD_DIR / Path(image_path).name)

        pothole_dict = {
            "id": report_id,
            "lat": latitude,
            "lng": longitude,
            "severity": severity,
            "road": road,
            "timestamp": ts,
            "status": "reported",
            "issue_type": issue_type,
            "image_path": image_abs_path,
        }
        try:
            result = send_pothole_report(pothole_dict)
            email_status = result.get("status", "unknown")
        except Exception as e:
            email_status = f"failed: {str(e)}"
    elif send_email and not EMAIL_AVAILABLE:
        email_status = "email service unavailable"

    return ReportResponse(
        id=report.id,
        latitude=report.latitude,
        longitude=report.longitude,
        issue_type=report.issue_type,
        severity=report.severity,
        timestamp=ts,
        status=report.status,
        image_path=report.image_path,
        email_status=email_status,
    )
