import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "moorcheh"))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "moorcheh/.env"))

fake_pothole = {
    "id":        1,
    "road":      "Yonge St",
    "lat":       43.653200,
    "lng":      -79.383200,
    "severity":  "high",
    "timestamp": "2025-03-14T10:30:00",
    "status":    "reported"
}

print("\n" + "="*50)
print("TEST 1 — 311 contact info")
print("="*50)
from department_router import get_311_contact
print(get_311_contact())

print("\n" + "="*50)
print("TEST 2 — Report subject line")
print("="*50)
from report_generator import generate_report_subject
print(generate_report_subject(fake_pothole))

print("\n" + "="*50)
print("TEST 3 — AI report email body (calls HF endpoint)")
print("="*50)
from report_generator import generate_report
body = generate_report(fake_pothole)
print(body)

print("\n" + "="*50)
print("TEST 4 — Chatbot: ask about Yonge St")
print("="*50)
from report_generator import generate_chat_response
answer = generate_chat_response(
    "Is it safe to drive on Yonge St right now?",
    [fake_pothole]
)
print(answer)

print("\n" + "="*50)
print("TEST 5 — Full email send (simulated)")
print("="*50)
from email_sender import send_pothole_report
result = send_pothole_report(fake_pothole)
print(f"Status: {result['status']}")

print("\n" + "="*50)
print("TEST 6 — Follow-up email")
print("="*50)
from report_generator import generate_followup_email
followup = generate_followup_email(fake_pothole, days_ago=5)
print(followup)

print("\n✓ All 311-specific tests done!")