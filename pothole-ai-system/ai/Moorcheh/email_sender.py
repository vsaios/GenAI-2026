import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from report_generator import generate_report, generate_report_subject
from department_router import get_311_email, get_311_name

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Set to False when you want real emails to go to 311
# Set to True to test — sends to your own email instead
TESTING_MODE = True

def send_pothole_report(pothole: dict) -> dict:
    """Generate AI report and send to 311 Toronto (or your test email)."""

    subject = generate_report_subject(pothole)
    body    = generate_report(pothole)

    # Full email body with GPS footer for the repair crew
    full_body = f"""To: {get_311_name()}

{body}

---
AUTOMATED SYSTEM DATA
Report ID:   #{pothole['id']}
Street:      {pothole['road']}, Toronto
GPS:         {round(pothole['lat'], 6)}, {round(pothole['lng'], 6)}
Severity:    {pothole['severity'].upper()}
Detected:    {pothole['timestamp']}
System:      Toronto Pothole AI Monitoring — dashcam detection
Maps link:   https://maps.google.com/?q={pothole['lat']},{pothole['lng']}
"""

    if TESTING_MODE:
        # Prints to terminal — safe for demos and testing
        print(f"\n{'='*60}")
        print(f"[SIMULATED EMAIL — would send to {get_311_email()}]")
        print(f"FROM:    {os.getenv('GMAIL_USER', 'pothole.ai@test.com')}")
        print(f"TO:      {get_311_email()}")
        print(f"SUBJECT: {subject}")
        print(f"\nBODY:\n{full_body}")
        print(f"{'='*60}\n")
        return {
            "subject":  subject,
            "body":     full_body,
            "sent_to":  get_311_email(),
            "status":   "simulated — set TESTING_MODE=False to send for real"
        }
    else:
        # Real Gmail send to 311@toronto.ca
        msg = MIMEText(full_body)
        msg["Subject"] = subject
        msg["From"]    = os.getenv("GMAIL_USER")
        msg["To"]      = get_311_email()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
            server.send_message(msg)

        print(f"[Email] Sent to 311 Toronto — subject: {subject}")
        return {
            "subject":  subject,
            "body":     full_body,
            "sent_to":  get_311_email(),
            "status":   "sent"
        }