import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from moorcheh_sdk import MoorchehClient

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
client = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))

print("🗑 Removing Golden Horseshoe point...")
for doc_id in ["pothole_63", "pothole_75"]:
    try:
        client.documents.delete(
            namespace_name="toronto_potholes",
            document_ids=[doc_id]
        )
        print(f"  ✓ Deleted {doc_id}")
        time.sleep(0.5)
    except Exception as e:
        print(f"  ⚠ Could not delete {doc_id}: {e}")

print("\n🌱 Adding downtown Toronto replacement...")
p = {
    "id": 63,
    "lat": 43.6481, "lng": -79.3878,
    "severity": "high", "issue_type": "road obstruction",
    "road": "Queen St W & Bay St",
    "timestamp": (datetime.utcnow() - timedelta(days=1, hours=4)).isoformat(),
    "status": "reported_to_311", "sent_to_311": True
}

text = (
    f"Road obstruction on {p['road']}. "
    f"Severity: HIGH. "
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
    print(f"  ✓ Added — {p['road']} (HIGH road obstruction)")
except Exception as e:
    print(f"  ✗ Failed: {e}")

print("\n✅ Done!")