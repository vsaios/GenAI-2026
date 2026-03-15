import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from moorcheh_sdk import MoorchehClient
from moorcheh_sdk.exceptions import ConflictError

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
client = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))

NAMESPACES = ["toronto_potholes", "pothole_images", "citywatch_reports"]

print("\n🧹 Cleaning namespaces...")
for ns in NAMESPACES:
    try:
        client.namespaces.delete(namespace_name=ns)
        print(f"  ✓ Deleted: {ns}")
        time.sleep(0.5)
    except Exception as e:
        print(f"  ⚠ Could not delete {ns}: {e}")

print("\n🔧 Recreating namespaces...")
for ns in NAMESPACES:
    try:
        client.namespaces.create(namespace_name=ns, type="text")
        print(f"  ✓ Created: {ns}")
        time.sleep(0.5)
    except ConflictError:
        print(f"  ✓ Already exists: {ns}")

DEMO_INCIDENTS = [
    # ── Downtown Toronto (25 points) ────────────────────────────
    {
        "id": 1, "lat": 43.6532, "lng": -79.3832,
        "severity": "high", "issue_type": "pothole",
        "road": "King St W & Spadina Ave",
        "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 2, "lat": 43.6510, "lng": -79.3790,
        "severity": "high", "issue_type": "pothole",
        "road": "Front St E & Church St",
        "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 3, "lat": 43.6489, "lng": -79.3923,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "Wellington St W & Simcoe St",
        "timestamp": (datetime.utcnow() - timedelta(hours=3)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 4, "lat": 43.6534, "lng": -79.3712,
        "severity": "high", "issue_type": "pothole",
        "road": "King St E & Parliament St",
        "timestamp": (datetime.utcnow() - timedelta(hours=4)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 5, "lat": 43.6567, "lng": -79.3845,
        "severity": "low", "issue_type": "broken streetlight",
        "road": "Richmond St W & Peter St",
        "timestamp": (datetime.utcnow() - timedelta(hours=6)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 6, "lat": 43.6612, "lng": -79.3934,
        "severity": "medium", "issue_type": "pothole",
        "road": "Dundas St W & McCaul St",
        "timestamp": (datetime.utcnow() - timedelta(hours=7)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 7, "lat": 43.6478, "lng": -79.3867,
        "severity": "high", "issue_type": "road obstruction",
        "road": "Queen St W & Bay St",
        "timestamp": (datetime.utcnow() - timedelta(hours=9)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 8, "lat": 43.6523, "lng": -79.4012,
        "severity": "medium", "issue_type": "illegal dumping",
        "road": "Bathurst St & King St W",
        "timestamp": (datetime.utcnow() - timedelta(hours=10)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 9, "lat": 43.6589, "lng": -79.3778,
        "severity": "low", "issue_type": "broken streetlight",
        "road": "Yonge St & Shuter St",
        "timestamp": (datetime.utcnow() - timedelta(hours=11)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 10, "lat": 43.6545, "lng": -79.3956,
        "severity": "high", "issue_type": "pothole",
        "road": "Queen St W & Spadina Ave",
        "timestamp": (datetime.utcnow() - timedelta(hours=13)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 11, "lat": 43.6498, "lng": -79.3701,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "Front St E & Jarvis St",
        "timestamp": (datetime.utcnow() - timedelta(hours=14)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 12, "lat": 43.6623, "lng": -79.3812,
        "severity": "low", "issue_type": "pothole",
        "road": "Dundas St E & Yonge St",
        "timestamp": (datetime.utcnow() - timedelta(hours=15)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 13, "lat": 43.6556, "lng": -79.4089,
        "severity": "high", "issue_type": "pothole",
        "road": "King St W & Strachan Ave",
        "timestamp": (datetime.utcnow() - timedelta(hours=16)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 14, "lat": 43.6467, "lng": -79.3978,
        "severity": "medium", "issue_type": "broken streetlight",
        "road": "Queen St W & University Ave",
        "timestamp": (datetime.utcnow() - timedelta(hours=18)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 15, "lat": 43.6601, "lng": -79.3712,
        "severity": "high", "issue_type": "road obstruction",
        "road": "Gerrard St E & Church St",
        "timestamp": (datetime.utcnow() - timedelta(hours=19)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 16, "lat": 43.6512, "lng": -79.3856,
        "severity": "low", "issue_type": "illegal dumping",
        "road": "Wellington St W & York St",
        "timestamp": (datetime.utcnow() - timedelta(hours=20)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 17, "lat": 43.6578, "lng": -79.3967,
        "severity": "medium", "issue_type": "pothole",
        "road": "College St & Spadina Ave",
        "timestamp": (datetime.utcnow() - timedelta(hours=21)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 18, "lat": 43.6634, "lng": -79.3889,
        "severity": "high", "issue_type": "pothole",
        "road": "Dundas St W & Beverley St",
        "timestamp": (datetime.utcnow() - timedelta(hours=22)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 19, "lat": 43.6487, "lng": -79.3745,
        "severity": "medium", "issue_type": "broken streetlight",
        "road": "Queen St E & Sherbourne St",
        "timestamp": (datetime.utcnow() - timedelta(hours=23)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 20, "lat": 43.6645, "lng": -79.4023,
        "severity": "low", "issue_type": "road obstruction",
        "road": "Bloor St W & Palmerston Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 21, "lat": 43.6519, "lng": -79.3912,
        "severity": "high", "issue_type": "pothole",
        "road": "Front St W & John St",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=1)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 22, "lat": 43.6592, "lng": -79.3823,
        "severity": "medium", "issue_type": "illegal dumping",
        "road": "Bond St & Dundas St E",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=2)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 23, "lat": 43.6471, "lng": -79.4034,
        "severity": "high", "issue_type": "pothole",
        "road": "Queen St W & Ossington Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=3)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 24, "lat": 43.6638, "lng": -79.3756,
        "severity": "low", "issue_type": "broken streetlight",
        "road": "Carlton St & Jarvis St",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=4)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 25, "lat": 43.6503, "lng": -79.3689,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "King St E & Sumach St",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=5)).isoformat(),
        "status": "reported", "sent_to_311": False
    },

    # ── Midtown Toronto ─────────────────────────────────────────
    {
        "id": 26, "lat": 43.6880, "lng": -79.3976,
        "severity": "high", "issue_type": "pothole",
        "road": "Eglinton Ave W & Allen Rd",
        "timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 27, "lat": 43.6923, "lng": -79.3847,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "Eglinton Ave E & Yonge St",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=12)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 28, "lat": 43.6795, "lng": -79.4089,
        "severity": "low", "issue_type": "broken streetlight",
        "road": "St Clair Ave W & Bathurst St",
        "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 29, "lat": 43.7012, "lng": -79.4231,
        "severity": "medium", "issue_type": "pothole",
        "road": "Lawrence Ave W & Dufferin St",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=4)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 30, "lat": 43.6756, "lng": -79.3543,
        "severity": "high", "issue_type": "road obstruction",
        "road": "Bayview Ave & Moore Ave",
        "timestamp": (datetime.utcnow() - timedelta(hours=9)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },

    # ── East Toronto / Danforth ──────────────────────────────────
    {
        "id": 31, "lat": 43.6762, "lng": -79.2903,
        "severity": "medium", "issue_type": "pothole",
        "road": "Danforth Ave & Woodbine Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=4)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 32, "lat": 43.6734, "lng": -79.3123,
        "severity": "high", "issue_type": "pothole",
        "road": "Danforth Ave & Pape Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=2)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 33, "lat": 43.6689, "lng": -79.2712,
        "severity": "low", "issue_type": "illegal dumping",
        "road": "Kingston Rd & Victoria Park Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=3, hours=6)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 34, "lat": 43.6821, "lng": -79.3312,
        "severity": "medium", "issue_type": "broken streetlight",
        "road": "Broadview Ave & Gerrard St E",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=8)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 35, "lat": 43.6645, "lng": -79.2534,
        "severity": "high", "issue_type": "road obstruction",
        "road": "Kingston Rd & Midland Ave",
        "timestamp": (datetime.utcnow() - timedelta(hours=14)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },

    # ── Scarborough ──────────────────────────────────────────────
    {
        "id": 36, "lat": 43.7615, "lng": -79.3300,
        "severity": "low", "issue_type": "pothole",
        "road": "Sheppard Ave E & Victoria Park Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=3, hours=2)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 37, "lat": 43.7734, "lng": -79.2578,
        "severity": "high", "issue_type": "pothole",
        "road": "Sheppard Ave E & McCowan Rd",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=7)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 38, "lat": 43.7812, "lng": -79.2234,
        "severity": "medium", "issue_type": "illegal dumping",
        "road": "Ellesmere Rd & Morningside Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=3)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 39, "lat": 43.7923, "lng": -79.2712,
        "severity": "high", "issue_type": "road obstruction",
        "road": "Finch Ave E & Kennedy Rd",
        "timestamp": (datetime.utcnow() - timedelta(hours=16)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 40, "lat": 43.7456, "lng": -79.2389,
        "severity": "medium", "issue_type": "broken streetlight",
        "road": "Lawrence Ave E & Birchmount Rd",
        "timestamp": (datetime.utcnow() - timedelta(days=4, hours=2)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 41, "lat": 43.7678, "lng": -79.1923,
        "severity": "low", "issue_type": "pothole",
        "road": "Sheppard Ave E & Orton Park Rd",
        "timestamp": (datetime.utcnow() - timedelta(days=5)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 42, "lat": 43.7534, "lng": -79.2812,
        "severity": "high", "issue_type": "pothole",
        "road": "Warden Ave & Lawrence Ave E",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=4)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },

    # ── North York ───────────────────────────────────────────────
    {
        "id": 43, "lat": 43.7731, "lng": -79.4130,
        "severity": "high", "issue_type": "pothole",
        "road": "Finch Ave W & Keele St",
        "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 44, "lat": 43.7612, "lng": -79.4523,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "Finch Ave W & Jane St",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=5)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 45, "lat": 43.7823, "lng": -79.3712,
        "severity": "low", "issue_type": "broken streetlight",
        "road": "Steeles Ave W & Dufferin St",
        "timestamp": (datetime.utcnow() - timedelta(days=4, hours=8)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 46, "lat": 43.7456, "lng": -79.4012,
        "severity": "high", "issue_type": "pothole",
        "road": "Wilson Ave & Allen Rd",
        "timestamp": (datetime.utcnow() - timedelta(hours=20)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 47, "lat": 43.7312, "lng": -79.3845,
        "severity": "medium", "issue_type": "illegal dumping",
        "road": "Lawrence Ave W & Yonge St",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=9)).isoformat(),
        "status": "reported", "sent_to_311": False
    },

    # ── Etobicoke ────────────────────────────────────────────────
    {
        "id": 48, "lat": 43.6435, "lng": -79.4282,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "Roncesvalles Ave & Howard Park Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=6)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 49, "lat": 43.6712, "lng": -79.5123,
        "severity": "high", "issue_type": "pothole",
        "road": "Bloor St W & Islington Ave",
        "timestamp": (datetime.utcnow() - timedelta(hours=11)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 50, "lat": 43.6534, "lng": -79.5489,
        "severity": "medium", "issue_type": "broken streetlight",
        "road": "Burnhamthorpe Rd & Kipling Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=3, hours=4)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 51, "lat": 43.7012, "lng": -79.5634,
        "severity": "low", "issue_type": "illegal dumping",
        "road": "Dixon Rd & Kipling Ave",
        "timestamp": (datetime.utcnow() - timedelta(days=4)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 52, "lat": 43.7234, "lng": -79.5312,
        "severity": "high", "issue_type": "pothole",
        "road": "Finch Ave W & Martingrove Rd",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=3)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },

    # ── Mississauga ──────────────────────────────────────────────
    {
        "id": 53, "lat": 43.5890, "lng": -79.6441,
        "severity": "high", "issue_type": "pothole",
        "road": "Hurontario St & Burnhamthorpe Rd",
        "timestamp": (datetime.utcnow() - timedelta(hours=7)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 54, "lat": 43.5723, "lng": -79.6234,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "Eglinton Ave W & Hurontario St",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=5)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 55, "lat": 43.6012, "lng": -79.6823,
        "severity": "low", "issue_type": "broken streetlight",
        "road": "Dundas St W & Erin Mills Pkwy",
        "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 56, "lat": 43.5534, "lng": -79.6634,
        "severity": "high", "issue_type": "pothole",
        "road": "Lakeshore Rd E & Dixie Rd",
        "timestamp": (datetime.utcnow() - timedelta(hours=13)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 57, "lat": 43.6234, "lng": -79.7123,
        "severity": "medium", "issue_type": "illegal dumping",
        "road": "Britannia Rd W & Creditview Rd",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=7)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 58, "lat": 43.5412, "lng": -79.5923,
        "severity": "low", "issue_type": "road obstruction",
        "road": "Lakeshore Rd W & Mississauga Rd",
        "timestamp": (datetime.utcnow() - timedelta(days=5)).isoformat(),
        "status": "reported", "sent_to_311": False
    },

    # ── Hamilton ─────────────────────────────────────────────────
    {
        "id": 59, "lat": 43.2557, "lng": -79.8711,
        "severity": "high", "issue_type": "pothole",
        "road": "Main St E & James St N, Hamilton",
        "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 60, "lat": 43.2623, "lng": -79.8923,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "King St W & Dundurn St, Hamilton",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=3)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 61, "lat": 43.2389, "lng": -79.8234,
        "severity": "high", "issue_type": "pothole",
        "road": "Barton St E & Kenilworth Ave, Hamilton",
        "timestamp": (datetime.utcnow() - timedelta(hours=10)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 62, "lat": 43.2712, "lng": -79.9123,
        "severity": "low", "issue_type": "broken streetlight",
        "road": "Mohawk Rd W & West 5th St, Hamilton",
        "timestamp": (datetime.utcnow() - timedelta(days=4)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 63, "lat": 43.2234, "lng": -79.7923,
        "severity": "medium", "issue_type": "illegal dumping",
        "road": "Queenston Rd & Centennial Pkwy, Hamilton",
        "timestamp": (datetime.utcnow() - timedelta(days=3, hours=5)).isoformat(),
        "status": "reported", "sent_to_311": False
    },

    # ── Brampton ─────────────────────────────────────────────────
    {
        "id": 64, "lat": 43.6834, "lng": -79.7612,
        "severity": "high", "issue_type": "pothole",
        "road": "Steeles Ave W & Airport Rd, Brampton",
        "timestamp": (datetime.utcnow() - timedelta(hours=15)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 65, "lat": 43.6423, "lng": -79.7234,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "Derry Rd W & Hurontario St, Brampton",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=1)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 66, "lat": 43.7123, "lng": -79.7534,
        "severity": "low", "issue_type": "broken streetlight",
        "road": "Queen St W & Chinguacousy Rd, Brampton",
        "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 67, "lat": 43.6956, "lng": -79.7812,
        "severity": "high", "issue_type": "pothole",
        "road": "Bovaird Dr W & Hurontario St, Brampton",
        "timestamp": (datetime.utcnow() - timedelta(hours=8)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },

    # ── Vaughan / North ──────────────────────────────────────────
    {
        "id": 68, "lat": 43.8334, "lng": -79.4989,
        "severity": "medium", "issue_type": "pothole",
        "road": "Highway 7 & Weston Rd, Vaughan",
        "timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 69, "lat": 43.8012, "lng": -79.5234,
        "severity": "high", "issue_type": "road obstruction",
        "road": "Rutherford Rd & Jane St, Vaughan",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=6)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },

    # ── Markham / East ───────────────────────────────────────────
    {
        "id": 70, "lat": 43.8534, "lng": -79.2612,
        "severity": "medium", "issue_type": "broken streetlight",
        "road": "Highway 7 & Warden Ave, Markham",
        "timestamp": (datetime.utcnow() - timedelta(days=3, hours=2)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 71, "lat": 43.8234, "lng": -79.2989,
        "severity": "high", "issue_type": "pothole",
        "road": "16th Ave & McCowan Rd, Markham",
        "timestamp": (datetime.utcnow() - timedelta(hours=5)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },

    # ── Oakville ─────────────────────────────────────────────────
    {
        "id": 72, "lat": 43.4675, "lng": -79.6877,
        "severity": "medium", "issue_type": "pothole",
        "road": "Lakeshore Rd E & Kerr St, Oakville",
        "timestamp": (datetime.utcnow() - timedelta(days=2, hours=4)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
    {
        "id": 73, "lat": 43.4823, "lng": -79.7123,
        "severity": "low", "issue_type": "illegal dumping",
        "road": "Dundas St E & Trafalgar Rd, Oakville",
        "timestamp": (datetime.utcnow() - timedelta(days=4)).isoformat(),
        "status": "reported", "sent_to_311": False
    },

    # ── Burlington ───────────────────────────────────────────────
    {
        "id": 74, "lat": 43.3734, "lng": -79.7989,
        "severity": "high", "issue_type": "pothole",
        "road": "Brant St & Fairview St, Burlington",
        "timestamp": (datetime.utcnow() - timedelta(hours=12)).isoformat(),
        "status": "reported_to_311", "sent_to_311": True
    },
    {
        "id": 75, "lat": 43.3512, "lng": -79.8234,
        "severity": "medium", "issue_type": "road obstruction",
        "road": "Lakeshore Rd & Guelph Line, Burlington",
        "timestamp": (datetime.utcnow() - timedelta(days=1, hours=8)).isoformat(),
        "status": "reported", "sent_to_311": False
    },
]

print("\n🌱 Seeding 75 incidents...")
for p in DEMO_INCIDENTS:
    issue = p.get("issue_type", "pothole")
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
        print(f"  ✓ #{p['id']} — {p['road']} ({p['severity'].upper()} {issue})")
        time.sleep(0.3)
    except Exception as e:
        print(f"  ✗ Failed #{p['id']}: {e}")

print("\n✅ Done!")
print(f"   Total: {len(DEMO_INCIDENTS)}")
print(f"   High:   {len([p for p in DEMO_INCIDENTS if p['severity'] == 'high'])}")
print(f"   Medium: {len([p for p in DEMO_INCIDENTS if p['severity'] == 'medium'])}")
print(f"   Low:    {len([p for p in DEMO_INCIDENTS if p['severity'] == 'low'])}")
print(f"   Sent to 311: {len([p for p in DEMO_INCIDENTS if p['sent_to_311']])}")