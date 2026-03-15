"""Syncs all SQLite reports into Moorcheh. Can be run standalone or called on startup."""
import sys
import os
import httpx

_here = os.path.dirname(os.path.abspath(__file__))
AI_PATH = os.path.normpath(os.path.join(_here, "..", "..", "ai", "Moorcheh"))
if AI_PATH not in sys.path:
    sys.path.insert(0, AI_PATH)

from database.db import engine
from database.models import ReportModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv(os.path.join(AI_PATH, ".env"))
GEOAPIFY_KEY = os.environ.get("GEOAPIFY_API_KEY", "")


def reverse_geocode(lat, lng):
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


def run_sync():
    try:
        from memory_client import save_pothole, get_all_potholes
    except Exception as e:
        print(f"[Sync] ✗ Could not import memory_client: {e}")
        return

    print("[Sync] 🔄 Syncing SQLite reports to Moorcheh...")

    # Get existing Moorcheh coords to avoid duplicates
    try:
        existing = get_all_potholes()
        existing_coords = set(
            (round(float(p.get("lat", 0)), 4), round(float(p.get("lng", 0)), 4))
            for p in existing
        )
        print(f"[Sync]    Found {len(existing_coords)} existing records in Moorcheh")
    except Exception as e:
        print(f"[Sync] ✗ Could not read Moorcheh: {e}")
        existing_coords = set()

    synced = 0
    skipped = 0

    with Session(engine) as db:
        rows = db.query(ReportModel).all()
        print(f"[Sync]    Found {len(rows)} reports in SQLite")

        for r in rows:
            coord_key = (round(r.latitude, 4), round(r.longitude, 4))

            # Skip duplicates
            if coord_key in existing_coords:
                skipped += 1
                continue

            try:
                road = reverse_geocode(r.latitude, r.longitude)
                save_pothole(
                    lat=r.latitude,
                    lng=r.longitude,
                    severity=r.severity,
                    road=road,
                    frame_timestamp=r.timestamp.isoformat(),
                )
                existing_coords.add(coord_key)
                print(f"[Sync]    ✓ Synced: {road} ({r.severity})")
                synced += 1
            except Exception as e:
                print(f"[Sync]    ✗ Failed {r.id}: {e}")

    print(f"[Sync] ✅ Done! Synced: {synced} | Skipped: {skipped}")


# Run standalone
if __name__ == "__main__":
    run_sync()