import sys
import os

_here = os.path.dirname(os.path.abspath(__file__))
AI_PATH = os.path.normpath(os.path.join(_here, "..", "..", "..", "ai", "Moorcheh"))
if AI_PATH not in sys.path:
    sys.path.insert(0, AI_PATH)

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from memory_client import get_potholes, get_summary, save_pothole, mark_sent_to_311
from report_generator import generate_chat_response
from email_sender import send_pothole_report

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class PotholeReport(BaseModel):
    lat: float
    lng: float
    severity: str
    road: str
    frame_timestamp: str = ""

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        all_potholes = get_potholes()
        answer = generate_chat_response(request.message, all_potholes)
        return {"answer": answer, "potholes_found": len(all_potholes)}
    except Exception as e:
        return {
            "answer": f"Chat service error: {str(e)}",
            "potholes_found": 0,
        }

@router.get("/potholes")
async def get_all_potholes():
    return get_potholes()

@router.get("/potholes/{road}")
async def get_potholes_by_road(road: str):
    return get_potholes(road)

@router.get("/summary")
async def summary():
    return get_summary()

# ✅ REMOVED: /api/reports GET and POST — handled by reports.py

@router.post("/report")
async def report_pothole(
    lat:             float                 = Form(None),
    lng:             float                 = Form(None),
    severity:        str                   = Form(None),
    road:            str                   = Form("Unknown Road"),
    frame_timestamp: str                   = Form(""),
    image:           Optional[UploadFile]  = File(None),
    data:            Optional[str]         = Form(None)
):
    """
    Automated dashcam endpoint.
    Saves to Moorcheh, generates AI email, sends to 311.
    """
    image_bytes    = None
    image_filename = "pothole_detection.jpg"

    if image:
        image_bytes    = await image.read()
        image_filename = image.filename or "pothole_detection.jpg"

    pothole = save_pothole(
        lat=lat or 43.6532,
        lng=lng or -79.3832,
        severity=severity or "medium",
        road=road,
        frame_timestamp=frame_timestamp,
        image_bytes=image_bytes,
        image_filename=image_filename
    )

    email_result = send_pothole_report(pothole)

    if email_result["status"] == "sent":
        mark_sent_to_311(pothole["id"])

    return {
        "pothole":      pothole,
        "email_status": email_result["status"],
        "sent_to":      email_result["sent_to"],
        "subject":      email_result["subject"]
    }