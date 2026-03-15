import os
import sys
import base64
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '.env')))

from moorcheh_sdk import MoorchehClient

client = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))

image_path = os.path.join(os.path.dirname(__file__), "test_pothole.jpg")
with open(image_path, "rb") as f:
    image_bytes = f.read()

image_base64 = base64.b64encode(image_bytes).decode("utf-8")

print(f"Image size:  {len(image_bytes)} bytes")
print(f"Base64 size: {len(image_base64)} chars")
print(f"Uploading to Moorcheh...")

try:
    result = client.documents.upload(
        namespace_name="pothole_images",   # ← correct namespace
        documents=[{
            "id":      "test_image_999",
            "text":    "Test pothole image base64 storage",
            "metadata": {
                "pothole_id":   999,
                "image_base64": image_base64,
                "filename":     "test_pothole.jpg"
            }
        }]
    )
    print(f"✓ SUCCESS — Moorcheh accepted base64 in pothole_images!")
    print(f"Result: {result}")
    print("RESULT: use_base64")

except Exception as e:
    print(f"✗ FAILED — {e}")
    print("RESULT: use_vision_memory")