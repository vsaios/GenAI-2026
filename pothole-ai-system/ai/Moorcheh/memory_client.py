import os
import time
from datetime import datetime
from dotenv import load_dotenv
from moorcheh_sdk import MoorchehClient
from moorcheh_sdk.exceptions import ConflictError

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

client    = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))
NAMESPACE = "toronto_potholes"

# Create namespace on startup — safe to run every time
try:
    client.namespaces.create(namespace_name=NAMESPACE, type="text")
    print(f"[Memory] Namespace '{NAMESPACE}' created")
except ConflictError:
    print(f"[Memory] Namespace '{NAMESPACE}' ready")


# ============================================================
# PUBLIC FUNCTIONS — backend calls these
# ============================================================

def save_pothole(lat: float, lng: float, severity: str, road: str, frame_timestamp: str = "") -> dict:
    """Save a detected Toronto pothole to Moorcheh memory."""
    pothole_id = _generate_id()
    record = {
        "id":              pothole_id,
        "lat":             lat,
        "lng":             lng,
        "severity":        severity.lower(),
        "road":            road,
        "city":            "Toronto",
        "timestamp":       datetime.utcnow().isoformat(),
        "frame_timestamp": frame_timestamp,
        "status":          "reported",
        "sent_to_311":     False
    }
    _moorcheh_write(pothole_id, record)
    print(f"[Memory] Saved pothole #{pothole_id} on {road}")
    return record

def get_potholes(road: str = None) -> list:
    """Get potholes, filtered by road name if provided."""
    return _moorcheh_read(query=road)

def get_all_potholes() -> list:
    """Get every pothole in the system."""
    return _moorcheh_read()

def get_potholes_by_severity(severity: str) -> list:
    """Get all potholes of a specific severity."""
    all_p = get_all_potholes()
    return [p for p in all_p if p.get("severity") == severity.lower()]

def mark_sent_to_311(pothole_id: int) -> dict:
    """Mark a pothole as reported to 311 — prevents duplicate emails."""
    return _moorcheh_update(pothole_id, {"sent_to_311": True, "status": "reported_to_311"})

def get_unsent_potholes() -> list:
    """Get potholes not yet reported to 311."""
    all_p = get_all_potholes()
    return [p for p in all_p if not p.get("sent_to_311", False)]

def get_summary() -> dict:
    """Count summary for chatbot and frontend dashboard."""
    all_p = get_all_potholes()
    return {
        "total":       len(all_p),
        "high":        len([p for p in all_p if p.get("severity") == "high"]),
        "medium":      len([p for p in all_p if p.get("severity") == "medium"]),
        "low":         len([p for p in all_p if p.get("severity") == "low"]),
        "sent_to_311": len([p for p in all_p if p.get("sent_to_311")]),
        "pending_311": len([p for p in all_p if not p.get("sent_to_311")]),
    }

def _generate_id() -> int:
    return len(get_all_potholes()) + 1


# ============================================================
# MOORCHEH SDK CALLS
# ============================================================

def _moorcheh_write(pothole_id: int, record: dict):
    """Store a pothole record in Moorcheh."""
    text = (
        f"Pothole on {record['road']} in Toronto. "
        f"Severity: {record['severity'].upper()}. "
        f"GPS: {record['lat']}, {record['lng']}. "
        f"Reported at {record['timestamp']}. "
        f"Status: {record['status']}."
    )
    client.documents.upload(
        namespace_name=NAMESPACE,
        documents=[{
            "id":       f"pothole_{pothole_id}",
            "text":     text,
            "metadata": record
        }]
    )
    time.sleep(1)

def _moorcheh_read(query: str = None) -> list:
    """Retrieve potholes from Moorcheh memory."""
    search_query = f"pothole on {query} Toronto" if query else "pothole Toronto"
    result = client.similarity_search.query(
        namespaces=[NAMESPACE],
        query=search_query,
        top_k=50
    )
    docs = result.get("results", [])
    # TEMPORARY — print first result to see exact structure
    if docs:
        print(f"[Debug] Raw result sample: {docs[0]}")
    # Extract nested metadata — fall back to full doc if not present
    def extract_metadata(doc):
        if "metadata" in doc and isinstance(doc["metadata"], dict) and "metadata" in doc["metadata"]:
            return doc["metadata"]["metadata"]
        elif "metadata" in doc:
            return doc["metadata"]
        else:
            return doc
    return [extract_metadata(doc) for doc in docs]

def _moorcheh_update(pothole_id: int, fields: dict) -> dict:
    """Update a pothole record by re-uploading with merged fields."""
    all_p  = get_all_potholes()
    record = next((p for p in all_p if p.get("id") == pothole_id), None)
    if not record:
        print(f"[Memory] Pothole #{pothole_id} not found")
        return {}
    updated = {**record, **fields}
    _moorcheh_write(pothole_id, updated)
    return updated