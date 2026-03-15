import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from moorcheh_sdk import MoorchehClient

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
client = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))

# ── Delete the two bad points ────────────────────────────────
print("🗑 Removing bad points...")
for doc_id in ["pothole_33", "pothole_63"]:
    try:
        client.documents.delete(
            namespace_name="toronto_potholes",
            document_ids=[doc_id]
        )
        print(f"  ✓ Deleted {doc_id}")
        time.sleep(0.5)
    except Exception as e:
        print(f"  ⚠ Could not delete {doc_id}: {e}")

# ── Add two Markham replacements ─────────────────────────────
REPLACEMENTS = [
    {
        "id": 33,
        "lat": 43.8534, "lng": -79.3012,
        "severity": "low", "issue_type": "illegal dumping",
        "road": "Markham Rd & Steeles Ave E, Markham",
        "timestamp": (datetime.utcnow() - timedelta(days=3, hours=6)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 63,
        "lat": 43.8712, "lng": -79.2689,
        "severity": "high", "issue_type": "road obstruction",
        "road": "Highway 7 & Woodbine Ave, Markham",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=4)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
]

print("\n🌱 Adding Markham replacements...")
for p in REPLACEMENTS:
    issue = p["issue_type"]
    text = (
        f"{issue.title()} on {p['road']}. "
        f"Severity: {p['severity'].upper()}. "
        f"GPS: {p['lat']}, {p['lng']}. "
        f"Reported at {p['timestamp']}. "
        f"Status: {p['status']}."
    )
    try:
        client.documents.upload(
            namespace_name="toronto_potholes",
            documents=[{
                "id":       f"pothole_{p['id']}",
                "text":     text,
                "metadata": {**p, "city": "Toronto", "frame_timestamp": ""}
            }]
        )
        print(f"  ✓ Added #{p['id']} — {p['road']} ({p['severity'].upper()} {issue})")
        time.sleep(0.5)
    except Exception as e:
        print(f"  ✗ Failed #{p['id']}: {e}")

print("\n✅ Done! Two bad points replaced with Markham locations.")