import sys
import os

_here = os.path.dirname(os.path.abspath(__file__))
AI_PATH = os.path.normpath(os.path.join(_here, "..", "..", "..", "ai", "Moorcheh"))
if AI_PATH not in sys.path:
    sys.path.insert(0, AI_PATH)

import httpx
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(os.path.join(AI_PATH, ".env"))

try:
    from report_generator import generate_chat_response
    CHAT_AVAILABLE = True
except Exception as e:
    print(f"[Chat] report_generator unavailable: {e}")
    CHAT_AVAILABLE = False

try:
    from memory_client import get_all_potholes, save_pothole, mark_sent_to_311
    MOORCHEH_AVAILABLE = True
except Exception as e:
    print(f"[Chat] memory_client unavailable: {e}")
    MOORCHEH_AVAILABLE = False

router = APIRouter()
GEOAPIFY_KEY = os.environ.get("GEOAPIFY_API_KEY", "")


def reverse_geocode(lat: float, lng: float) -> str:
    if not GEOAPIFY_KEY:
        return f"{lat:.4f}, {lng:.4f}"
    try:
        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lng}&apiKey={GEOAPIFY_KEY}"
        resp = httpx.get(url, timeout=5)
        data = resp.json()
        props = data.get("features", [{}])[0].get("properties", {})
        street = props.get("street", "")
        city = props.get("city", "Toronto")
        return f"{street}, {city}" if street else f"{lat:.4f}, {lng:.4f}"
    except Exception:
        return f"{lat:.4f}, {lng:.4f}"


def build_pothole_list() -> list:
    """
    Read from Moorcheh. For any record with a bad road name
    (missing or literally 'pothole'), reverse geocode the coords.
    """
    if not MOORCHEH_AVAILABLE:
        return []

    try:
        records = get_all_potholes()
    except Exception as e:
        print(f"[Chat] Could not read Moorcheh: {e}")
        return []

    potholes = []
    for r in records:
        lat = float(r.get("lat", 0))
        lng = float(r.get("lng", 0))
        road = r.get("road", "")

        # Fix bad road names
        if not road or road.lower().strip() == "pothole" or "pothole" == road.lower().strip():
            road = reverse_geocode(lat, lng)

        potholes.append({
            "road":       road,
            "lat":        lat,
            "lng":        lng,
            "severity":   r.get("severity", "medium"),
            "timestamp":  r.get("timestamp", ""),
            "status":     r.get("status", "reported"),
            "issue_type": r.get("issue_type", "pothole"),
        })

    print(f"[Chat] Loaded {len(potholes)} potholes from Moorcheh")
    for p in potholes:
        print(f"  → {p['road']} | {p['severity']}")

    return potholes


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        all_potholes = build_pothole_list()
        if not CHAT_AVAILABLE:
            return {
                "answer": f"Chat service unavailable. {len(all_potholes)} potholes in system.",
                "potholes_found": len(all_potholes)
            }
        answer = generate_chat_response(request.message, all_potholes)
        return {"answer": answer, "potholes_found": len(all_potholes)}
    except Exception as e:
        return {
            "answer": f"Chat service error: {str(e)}",
            "potholes_found": 0,
        }


@router.get("/potholes")
async def get_all_potholes_route():
    return build_pothole_list()


@router.get("/potholes/{road}")
async def get_potholes_by_road(road: str):
    all_p = build_pothole_list()
    return [p for p in all_p if road.lower() in p.get("road", "").lower()]


@router.get("/summary")
async def summary():
    all_p = build_pothole_list()
    return {
        "total":  len(all_p),
        "high":   len([p for p in all_p if p.get("severity") == "high"]),
        "medium": len([p for p in all_p if p.get("severity") == "medium"]),
        "low":    len([p for p in all_p if p.get("severity") == "low"]),
    }


@router.post("/report")
async def report_pothole_dashcam(
    lat:             float = None,
    lng:             float = None,
    severity:        str   = None,
    road:            str   = "Unknown Road",
    frame_timestamp: str   = "",
):
    """Automated dashcam endpoint — saves to Moorcheh."""
    if not MOORCHEH_AVAILABLE:
        return {"error": "Moorcheh unavailable"}

    from email_sender import send_pothole_report

    pothole = save_pothole(
        lat=lat or 43.6532,
        lng=lng or -79.3832,
        severity=severity or "medium",
        road=road,
        frame_timestamp=frame_timestamp,
    )

    try:
        email_result = send_pothole_report(pothole)
        if email_result["status"] == "sent":
            mark_sent_to_311(pothole["id"])
    except Exception as e:
        email_result = {"status": f"failed: {e}", "sent_to": "", "subject": ""}

    return {
        "pothole":      pothole,
        "email_status": email_result["status"],
        "sent_to":      email_result.get("sent_to", ""),
        "subject":      email_result.get("subject", ""),
    }
