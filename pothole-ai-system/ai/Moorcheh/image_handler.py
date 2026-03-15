import os
import base64
import time
from dotenv import load_dotenv
from moorcheh_sdk import MoorchehClient
from moorcheh_sdk.exceptions import ConflictError

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

client          = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))
IMAGE_NAMESPACE = "pothole_images"

try:
    client.namespaces.create(namespace_name=IMAGE_NAMESPACE, type="text")
    print(f"[Image] Namespace '{IMAGE_NAMESPACE}' created")
except ConflictError:
    print(f"[Image] Namespace '{IMAGE_NAMESPACE}' ready")


def encode_image(image_bytes: bytes) -> str:
    """Convert raw image bytes to base64 string for Moorcheh storage."""
    return base64.b64encode(image_bytes).decode("utf-8")

def decode_image(image_base64: str) -> bytes:
    """Convert base64 string from Moorcheh back to raw image bytes."""
    return base64.b64decode(image_base64)

def store_image_in_moorcheh(pothole_id: int, image_bytes: bytes, filename: str = "pothole.jpg") -> dict:
    """
    Step 1 — encode image bytes to base64 string
    Step 2 — upload to Moorcheh pothole_images namespace
    Step 3 — return record with base64 for email attachment
    """
    print(f"[Image] Encoding {len(image_bytes)} bytes...")
    image_base64 = encode_image(image_bytes)
    print(f"[Image] Encoded to {len(image_base64)} chars")

    record = {
        "pothole_id":   pothole_id,
        "filename":     filename,
        "image_base64": image_base64,
        "size_bytes":   len(image_bytes),
        "size_base64":  len(image_base64)
    }

    client.documents.upload(
        namespace_name=IMAGE_NAMESPACE,
        documents=[{
            "id":       f"image_{pothole_id}",
            "text":     f"Pothole image for report #{pothole_id} detected on Toronto road",
            "metadata": record
        }]
    )
    time.sleep(1)
    print(f"[Image] ✓ Stored in Moorcheh for pothole #{pothole_id}")
    return record

def retrieve_image_from_moorcheh(pothole_id: int) -> dict:
    """
    Step 1 — search Moorcheh pothole_images namespace
    Step 2 — find exact match by pothole_id
    Step 3 — decode base64 back to bytes for email
    """
    result = client.similarity_search.query(
        namespaces=[IMAGE_NAMESPACE],
        query=f"pothole image report {pothole_id}",
        top_k=20
    )
    docs = result.get("results", [])

    for doc in docs:
        metadata = doc.get("metadata") or {}
        if metadata.get("pothole_id") == pothole_id:
            image_base64 = metadata.get("image_base64")
            if image_base64:
                image_bytes = decode_image(image_base64)
                print(f"[Image] ✓ Retrieved and decoded image for pothole #{pothole_id}")
                return {
                    "found":        True,
                    "pothole_id":   pothole_id,
                    "filename":     metadata.get("filename", "pothole.jpg"),
                    "image_base64": image_base64,
                    "image_bytes":  image_bytes
                }

    print(f"[Image] No image found for pothole #{pothole_id}")
    return {"found": False}