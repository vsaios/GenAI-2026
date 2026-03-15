import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from moorcheh_sdk import MoorchehClient
from moorcheh_sdk.exceptions import ConflictError

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

client = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))

NAMESPACES = ["toronto_potholes", "pothole_images", "citywatch_reports"]

# ============================================================
# STEP 1 — CLEAN ALL NAMESPACES
# ============================================================

print("\n🧹 Cleaning namespaces...")
for ns in NAMESPACES:
    try:
        client.namespaces.delete(namespace_name=ns)
        print(f"  ✓ Deleted: {ns}")
        time.sleep(1)
    except Exception as e:
        print(f"  ⚠ Could not delete {ns}: {e}")

# ============================================================
# STEP 2 — RECREATE NAMESPACES
# ============================================================

print("\n🔧 Recreating namespaces...")
for ns in NAMESPACES:
    try:
        client.namespaces.create(namespace_name=ns, type="text")
        print(f"  ✓ Created: {ns}")
        time.sleep(1)
    except ConflictError:
        print(f"  ✓ Already exists: {ns}")

# ============================================================
# STEP 3 — SEED DEMO POTHOLES
# ============================================================

DEMO_POTHOLES = [
    {
        "id": 1,
        "lat": 43.6532, "lng": -79.3832,
        "severity": "high",
        "road": "King St W & Spadina Ave",
        "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 2,
        "lat": 43.6629, "lng": -79.3957,
        "severity": "high",
        "road": "Bloor St W & Bathurst St",
        "timestamp": (datetime.utcnow() - timedelta(hours=5)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 3,
        "lat": 43.6478, "lng": -79.3733,
        "severity": "medium",
        "road": "Queen St E & Parliament St",
        "timestamp": (datetime.utcnow() - timedelta(hours=8)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 4,
        "lat": 43.6701, "lng": -79.3862,
        "severity": "medium",
        "road": "Yonge St & Davenport Rd",
        "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 5,
        "lat": 43.6544, "lng": -79.4100,
        "severity": "low",
        "road": "Dundas St W & Ossington Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=3)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 6,
        "lat": 43.6880, "lng": -79.3976,
        "severity": "high",
        "road": "Eglinton Ave W & Allen Rd",
        "timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 7,
        "lat": 43.6435, "lng": -79.4282,
        "severity": "medium",
        "road": "Roncesvalles Ave & Howard Park Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=6)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 8,
        "lat": 43.7731, "lng": -79.4130,
        "severity": "high",
        "road": "Finch Ave W & Keele St",
        "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 9,
        "lat": 43.7615, "lng": -79.3300,
        "severity": "low",
        "road": "Sheppard Ave E & Victoria Park Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=3, hours=2)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 10,
        "lat": 43.6762, "lng": -79.2903,
        "severity": "medium",
        "road": "Danforth Ave & Woodbine Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=4)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
]

print("\n🌱 Seeding demo potholes...")
for p in DEMO_POTHOLES:
    text = (
        f"Pothole on {p['road']} in Toronto. "
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
        print(f"  ✓ #{p['id']} — {p['road']} ({p['severity'].upper()})")
        time.sleep(1)
    except Exception as e:
        print(f"  ✗ Failed #{p['id']}: {e}")

print("\n✅ Done! Demo data ready.")
print(f"   Total potholes seeded: {len(DEMO_POTHOLES)}")
print(f"   High: {len([p for p in DEMO_POTHOLES if p['severity'] == 'high'])}")
print(f"   Medium: {len([p for p in DEMO_POTHOLES if p['severity'] == 'medium'])}")
print(f"   Low: {len([p for p in DEMO_POTHOLES if p['severity'] == 'low'])}")
print(f"   Sent to 311: {len([p for p in DEMO_POTHOLES if p['sent_to_311']])}")