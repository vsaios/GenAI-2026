import os
import base64
import smtplib
import mimetypes
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from report_generator import generate_report, generate_report_subject
from department_router import get_311_email, get_311_name

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

TESTING_MODE = True

def send_pothole_report(pothole: dict) -> dict:
    """
    Generate AI report and email to 311 Toronto.
    Supports two image sources:
    1. image_base64 — automated detection stored in Moorcheh
    2. image_path   — self reported image from file path
    """
    subject  = generate_report_subject(pothole)
    body     = generate_report(pothole)
    maps_url = f"https://maps.google.com/?q={pothole['lat']},{pothole['lng']}"

    if pothole.get("image_base64"):
        image_line = "Image: Attached — AI detected dashcam frame from Moorcheh"
    elif pothole.get("image_path"):
        image_line = "Image: Attached — self reported by user"
    else:
        image_line = "Image: Not available"

    issue_type = pothole.get("issue_type", "pothole").title()

    full_body = f"""To: {get_311_name()}

{body}

---
AUTOMATED SYSTEM DATA
Report ID:   #{pothole['id']}
Issue Type:  {issue_type}
Street:      {pothole['road']}, Toronto
GPS:         {round(pothole['lat'], 6)}, {round(pothole['lng'], 6)}
Severity:    {pothole['severity'].upper()}
Detected:    {pothole['timestamp']}
Maps link:   {maps_url}
{image_line}
System:      StreetSafe Toronto — AI Pothole Monitoring
"""

    recipient = os.getenv("TEST_EMAIL") if TESTING_MODE else os.getenv("TO_EMAIL", "311@toronto.ca")

    try:
        _send_gmail_with_image(
            to=recipient,
            subject=subject,
            body=full_body,
            image_base64=pothole.get("image_base64"),
            image_filename=pothole.get("image_filename", "pothole.jpg"),
            image_path=pothole.get("image_path")
        )
        print(f"[Email] ✓ Sent to {recipient}")
        return {
            "subject":  subject,
            "body":     full_body,
            "sent_to":  recipient,
            "status":   "sent",
            "testing":  TESTING_MODE
        }
    except Exception as e:
        print(f"[Email] ✗ Failed: {e}")
        return {
            "subject":  subject,
            "body":     full_body,
            "sent_to":  recipient,
            "status":   f"failed: {str(e)}",
            "testing":  TESTING_MODE
        }


def _send_gmail_with_image(to: str, subject: str, body: str,
                            image_base64: str = None,
                            image_filename: str = "pothole_detection.jpg",
                            image_path: str = None):
    """
    Send email via Gmail SMTP.
    Source 1: image_base64 — from Moorcheh (automated AI detection)
    Source 2: image_path   — from file system (self reported)
    Priority: base64 first, file path as fallback
    """
    gmail_user     = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_password:
        raise ValueError("GMAIL_USER or GMAIL_APP_PASSWORD not set in .env")

    msg            = MIMEMultipart()
    msg["From"]    = gmail_user
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Source 1 — base64 from Moorcheh (automated dashcam detection)
    if image_base64:
        try:
            image_bytes      = base64.b64decode(image_base64)
            image_attachment = MIMEImage(image_bytes)
            image_attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=image_filename
            )
            msg.attach(image_attachment)
            print(f"[Email] ✓ Dashcam image attached from Moorcheh: {image_filename}")
        except Exception as e:
            print(f"[Email] ⚠ Could not attach Moorcheh image: {e}")

    # Source 2 — file path (self reported by user)
    elif image_path and os.path.isfile(image_path):
        try:
            mime_type, _ = mimetypes.guess_type(image_path)
            if mime_type and mime_type.startswith("image/"):
                maintype, subtype = mime_type.split("/", 1)
            else:
                maintype, subtype = "application", "octet-stream"

            with open(image_path, "rb") as f:
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(f.read())

            encoders.encode_base64(attachment)
            filename = os.path.basename(image_path)
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(attachment)
            print(f"[Email] ✓ Self-reported image attached from path: {filename}")
        except Exception as e:
            print(f"[Email] ⚠ Could not attach self-reported image: {e}")

    else:
        print("[Email] No image to attach")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.send_message(msg)