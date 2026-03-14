import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '.env')))

from openai import OpenAI
client = OpenAI(api_key='hf-no-key-needed', base_url='https://vjioo4r1vyvcozuj.us-east-2.aws.endpoints.huggingface.cloud/v1')
models = client.models.list()
for m in models:
    print(m.id)
# ============================================================
# TEST 1 — Save a pothole to Moorcheh
# ============================================================
print("\n" + "="*60)
print("TEST 1 — Save pothole to Moorcheh memory")
print("="*60)

from memory_client import save_pothole, get_potholes, get_summary

pothole = save_pothole(
    lat=43.6532,
    lng=-79.3832,
    severity="high",
    road="Yonge St"
)
print(f"✓ Saved: {pothole}")

# ============================================================
# TEST 2 — Retrieve it back from Moorcheh
# ============================================================
print("\n" + "="*60)
print("TEST 2 — Retrieve potholes from Moorcheh")
print("="*60)

time.sleep(2)
results = get_potholes("Yonge St")
print(f"✓ Found {len(results)} pothole(s) on Yonge St")
for r in results:
    print(f"  - Road: {r.get('road')} | Severity: {r.get('severity')} | ID: {r.get('id')}")

summary = get_summary()
print(f"✓ Summary: {summary}")

# ============================================================
# TEST 3 — AI generates 311 report email
# ============================================================
print("\n" + "="*60)
print("TEST 3 — AI generates 311 report email (calls HF endpoint)")
print("="*60)

from report_generator import generate_report, generate_report_subject

subject = generate_report_subject(pothole)
print(f"✓ Subject: {subject}")

body = generate_report(pothole)
print(f"✓ Email body:\n{body}")

# ============================================================
# TEST 4 — Chatbot answers road safety questions
# ============================================================
print("\n" + "="*60)
print("TEST 4 — Chatbot answers road safety questions")
print("="*60)

from report_generator import generate_chat_response

all_potholes = get_potholes()
questions = [
    "Is it safe to drive on Yonge St right now?",
    "Which roads have the most dangerous potholes?",
    "Should I avoid any streets today?"
]

for q in questions:
    print(f"\n  User: {q}")
    answer = generate_chat_response(q, all_potholes)
    print(f"  Bot:  {answer}")

print("\n" + "="*60)
print("✓ ALL TESTS DONE")
print("="*60)
print("\nNext step: set up email when ready")
print("  → make a Gmail app password")
print("  → add GMAIL_USER and GMAIL_APP_PASSWORD to .env")
print("  → run test_email.py separately")