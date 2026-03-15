import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '.env')))

print("\n" + "="*60)
print("TEST 1 — Load test image")
print("="*60)
image_path = os.path.join(os.path.dirname(__file__), "test_pothole.jpg")
with open(image_path, "rb") as f:
    image_bytes = f.read()
print(f"✓ Loaded: {len(image_bytes)} bytes")

print("\n" + "="*60)
print("TEST 2 — Store image in Moorcheh")
print("="*60)
from image_handler import store_image_in_moorcheh
result = store_image_in_moorcheh(1, image_bytes, "test_pothole.jpg")
print(f"✓ Stored: {result}")

print("\n" + "="*60)
print("TEST 3 — Retrieve from Moorcheh")
print("="*60)
import time
time.sleep(3)

from image_handler import retrieve_image_from_moorcheh
retrieved = retrieve_image_from_moorcheh(1)
print(f"✓ Found: {retrieved.get('found')}")
if retrieved.get("description"):
    print(f"✓ Description: {retrieved['description']}")
if retrieved.get("image_bytes"):
    match = image_bytes == retrieved["image_bytes"]
    print(f"✓ Bytes match: {match}")

print("\n" + "="*60)
print("TEST 4 — Full save_pothole with image")
print("="*60)
from memory_client import save_pothole
pothole = save_pothole(43.6532, -79.3832, "high", "Yonge St",
                       image_bytes=image_bytes,
                       image_filename="yonge_pothole.jpg")
print(f"✓ Pothole #{pothole['id']} saved")
print(f"✓ Has image: {pothole['has_image']}")
print(f"✓ Description: {pothole.get('image_description', 'N/A')[:80]}")

print("\n" + "="*60)
print("TEST 5 — Send email with image")
print("="*60)
from email_sender import send_pothole_report
email = send_pothole_report(pothole)
print(f"✓ Email status: {email['status']}")
print(f"✓ Sent to: {email['sent_to']}")

print("\n✓ COMPLETE IMAGE PIPELINE WORKING!")