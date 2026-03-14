import sys
import os

AI_PATH = r"C:\GenAI-2026---Project-pothole\pothole-ai-system\ai\Moorcheh"
if AI_PATH not in sys.path:
    sys.path.insert(0, AI_PATH)

from fastapi import APIRouter
from pydantic import BaseModel
from memory_client import get_potholes, get_summary
from report_generator import generate_chat_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    all_potholes = get_potholes()
    answer = generate_chat_response(request.message, all_potholes)
    return {"answer": answer, "potholes_found": len(all_potholes)}

@router.get("/potholes")
async def get_all_potholes():
    return get_potholes()

@router.get("/potholes/{road}")
async def get_potholes_by_road(road: str):
    return get_potholes(road)

@router.get("/summary")
async def summary():
    return get_summary()