# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0
import secrets
import string
import json
import os
import cv2
import base64
import time
from dotenv import load_dotenv
from datetime import datetime, timezone
from arduino.app_utils import App
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from arduino.app_peripherals.camera import WebSocketCamera
from arduino.app_utils.image import resized
from moorcheh_sdk import MoorchehClient
from moorcheh_sdk.exceptions import ConflictError

def check_dependencies():
    required = {
        "dotenv": "python-dotenv",
        "moorcheh_sdk": "moorcheh-sdk",
        "requests": "requests",
        "cv2": "opencv-python",
    }
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    if missing:
        raise RuntimeError(f"Missing dependencies: {', '.join(missing)}. Add them to requirements.txt")
    else:
        print("[Startup] All dependencies OK")

check_dependencies()




load_dotenv()

MOORCHEH_API_KEY = os.environ.get("MOORCHEH_API_KEY")
MOORCHEH_NAMESPACE = "pothole_images"

print(f"[Startup] API key loaded: {'YES' if MOORCHEH_API_KEY else 'NO'} — {MOORCHEH_API_KEY[:6]}...")

# Device/location config
DEVICE_ID = os.environ.get("DEVICE_ID", "dev_unknown")
LOCATION = {"lat": 43.6532, "lng": -79.3832}

# Image/save config
IMAGE_SAVE_CLASSES = {"bottle"}
IMAGE_SAVE_CONFIDENCE = 0.5
IMAGE_DEBOUNCE_SEC = 3.0
IMAGE_DIR = "detections/images"
LOG_FILE = "detections_log.json"
last_image_saved = {}

# UI / camera setup
secret = str(123456)
ui = WebUI()
resolution = (960, 1280)
camera = WebSocketCamera(resolution=resolution, secret=secret, encrypt=True, adjustments=resized(resolution, maintain_ratio=True))
camera.on_status_changed(lambda evt_type, data: ui.send_message(evt_type, data))
detection = VideoObjectDetection(camera, confidence=0.5, debounce_sec=0.0)
ui.on_connect(lambda sid: ui.send_message("welcome", {"client_name": camera.name, "secret": secret, "status": camera.status, "protocol": camera.protocol, "ip": camera.ip, "port": camera.port}))
ui.on_message("override_th", lambda sid, threshold: detection.override_threshold(threshold))

# Ensure dirs and logs
import shutil
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)
if os.path.exists(IMAGE_DIR):
    shutil.rmtree(IMAGE_DIR)
os.makedirs(IMAGE_DIR, exist_ok=True)

detections_log = []

# Moorcheh client and namespace creation (idempotent)
client = MoorchehClient(api_key=MOORCHEH_API_KEY)
try:
    client.namespaces.create(namespace_name=MOORCHEH_NAMESPACE, type="text")
    print(f"[Moorcheh] Namespace '{MOORCHEH_NAMESPACE}' created")
except ConflictError:
    print(f"[Moorcheh] Namespace '{MOORCHEH_NAMESPACE}' ready")
except Exception as e:
    print(f"[Moorcheh] Namespace creation warning: {e}")

def _encode_image_bytes(bytes_buf: bytes) -> str:
    return base64.b64encode(bytes_buf).decode("utf-8")

def _make_image_record(entry: dict, filename: str, image_bytes: bytes) -> dict:
    image_b64 = _encode_image_bytes(image_bytes) if image_bytes is not None else None
    record = {
        "pothole_id":   f"{DEVICE_ID}_{entry['timestamp']}",
        "filename":     filename,
        "image_base64": image_b64,
        "size_bytes":   len(image_bytes) if image_bytes else 0,
        "size_base64":  len(image_b64) if image_b64 else 0,
        # include detection/location fields for easier filtering
        "device_id":    DEVICE_ID,
        "lat":          entry.get("location", {}).get("lat"),
        "lng":          entry.get("location", {}).get("lng"),
        "label":        entry.get("label"),
        "confidence":   entry.get("confidence"),
        "bounding_box": entry.get("bounding_box"),
        "timestamp":    entry.get("timestamp"),
    }
    return record

def send_to_moorcheh_image(entry: dict, image_bytes: bytes = None, filename: str = "detection.jpg"):
    try:
        record = _make_image_record(entry, filename, image_bytes)
        doc_id = record["pothole_id"]

        # Serialize all fields into the text field since metadata is not supported
        doc_text = (
            f"label={entry.get('label')} "
            f"confidence={entry.get('confidence')} "
            f"lat={entry.get('location', {}).get('lat')} "
            f"lng={entry.get('location', {}).get('lng')} "
            f"timestamp={entry.get('timestamp')} "
            f"device={DEVICE_ID} "
            f"image={record.get('image_base64', '')}"
        )

        with MoorchehClient(api_key=MOORCHEH_API_KEY) as client:
            client.documents.upload(
                namespace_name=MOORCHEH_NAMESPACE,
                documents=[{"id": doc_id, "text": doc_text}]
            )
        print(f"[Moorcheh] Uploaded: {doc_id}")
    except Exception as e:
        print(f"[Moorcheh] Failed to upload {entry.get('timestamp')}: {e}")

def save_detections_to_file_and_store(detections: dict):
    now = datetime.now(timezone.utc).isoformat()

    for key, value_list in detections.items():
        best = max(value_list, key=lambda x: x.get("confidence", 0))
        confidence = best.get("confidence", 0)

        image_b64 = None
        image_bytes = None
        filename = None

        if key in IMAGE_SAVE_CLASSES and confidence >= IMAGE_SAVE_CONFIDENCE:
            time_since_last = time.time() - last_image_saved.get(key, 0)
            if time_since_last >= IMAGE_DEBOUNCE_SEC:
                try:
                    frame = camera.capture()
                    if frame is not None:
                        success, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                        if success:
                            image_bytes = buffer.tobytes()
                            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                            last_image_saved[key] = time.time()
                            filename = f"{key}_{int(time.time())}.jpg"
                            # save local copy (optional)
                            with open(os.path.join(IMAGE_DIR, filename), "wb") as wf:
                                wf.write(image_bytes)
                except Exception as e:
                    print(f"Failed to save image: {e}")

        entry = {
            "timestamp":    now,
            "label":        key,
            "confidence":   confidence,
            "bounding_box": best.get("bounding_box_xyxy"),
            "location":     LOCATION,
            "image_base64": image_b64,
        }

        detections_log.append(entry)
        with open(LOG_FILE, "w") as f:
            json.dump(detections_log, f, indent=2)

        # If we have an image, upload to Moorcheh pothole_images
        if image_bytes:
            send_to_moorcheh_image(entry, image_bytes=image_bytes, filename=filename)

    return entry

def send_detections_to_ui(detections: dict):
    for key, value_list in detections.items():
        best = max(value_list, key=lambda x: x.get("confidence", 0))
        msg = {
            "content": key,
            "confidence": best.get("confidence"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        ui.send_message("detection", msg)
    saved_entry = save_detections_to_file_and_store(detections)
    return saved_entry

detection.on_detect_all(send_detections_to_ui)
App.run()