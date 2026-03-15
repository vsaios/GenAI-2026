import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '.env')))

print("\n" + "="*60)
print("TEST 1 — Check credentials are loaded")
print("="*60)
gmail_user = os.getenv("GMAIL_USER")
gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
test_email = os.getenv("TEST_EMAIL")
print(f"GMAIL_USER:     {gmail_user}")
print(f"GMAIL_PASSWORD: {'SET' if gmail_pass else 'MISSING'}")
print(f"TEST_EMAIL:     {test_email}")

if not gmail_user or not gmail_pass:
    print("\n✗ Credentials missing — check your .env file")
    sys.exit(1)

print("\n" + "="*60)
print("TEST 2 — Generate AI email content")
print("="*60)
from report_generator import generate_report, generate_report_subject

fake_pothole = {
    "id":        99,
    "road":      "Yonge St",
    "lat":       43.6532,
    "lng":      -79.3832,
    "severity":  "high",
    "timestamp": "2026-03-14T20:00:00",
    "status":    "reported"
}

subject = generate_report_subject(fake_pothole)
body    = generate_report(fake_pothole)
print(f"✓ Subject: {subject}")
print(f"✓ Body preview: {body[:150]}...")

print("\n" + "="*60)
print("TEST 3 — Send real email to TEST_EMAIL")
print("="*60)
from email_sender import send_pothole_report

result = send_pothole_report(fake_pothole)
print(f"✓ Status:  {result['status']}")
print(f"✓ Sent to: {result['sent_to']}")
print(f"✓ Subject: {result['subject']}")

if result['status'] == 'sent':
    print(f"\n✓ CHECK YOUR EMAIL INBOX AT: {result['sent_to']}")
    print("✓ Email pipeline is fully working!")
else:
    print(f"\n✗ Email failed: {result['status']}")