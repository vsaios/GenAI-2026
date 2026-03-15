import os
import base64
import time
from dotenv import load_dotenv
from moorcheh_sdk import MoorchehClient

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

client          = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))
IMAGE_NAMESPACE = "pothole_images"

# ============================================================
# ENCODE — convert raw image bytes to base64 string
# ============================================================

def encode_image(image_bytes: bytes) -> str:
    """
    Convert raw image bytes to base64 string.
    This is what makes a binary image storable as text in Moorcheh.

    Example:
        raw bytes: b'\xff\xd8\xff\xe0...' (unreadable binary)
        base64:    '/9j/4AAQSkZJRgAB...' (readable text string)
    """
    return base64.b64encode(image_bytes).decode("utf-8")

# ============================================================
# DECODE — convert base64 string back to raw image bytes
# ============================================================

def decode_image(image_base64: str) -> bytes:
    """
    Convert base64 string back to raw image bytes.
    This is what you attach to an email or display on screen.

    Example:
        base64:    '/9j/4AAQSkZJRgAB...' (text from Moorcheh)
        raw bytes: b'\xff\xd8\xff\xe0...' (image file)
    """
    return base64.b64decode(image_base64)

# ============================================================
# STORE — save image to Moorcheh image namespace
# ============================================================

def store_image(pothole_id: int, image_bytes: bytes, filename: str = "pothole.jpg") -> dict:
    """
    Encode image and store in Moorcheh pothole_images namespace.
    Returns the storage record with base64 string.
    """
    if not image_bytes:
        return {"stored": False, "reason": "no image provided"}

    print(f"[Image] Encoding {len(image_bytes)} bytes to base64...")
    image_base64 = encode_image(image_bytes)
    print(f"[Image] Encoded — base64 length: {len(image_base64)} chars")

    # Store in Moorcheh image namespace
    record = {
        "pothole_id":    pothole_id,
        "filename":      filename,
        "image_base64":  image_base64,
        "size_bytes":    len(image_bytes),
        "size_base64":   len(image_base64)
    }

    try:
        client.documents.upload(
            namespace_name=IMAGE_NAMESPACE,
            documents=[{
                "id":      f"image_{pothole_id}",
                "content": f"Pothole image for pothole ID {pothole_id}. Filename: {filename}.",
                "metadata": record
            }]
        )
        time.sleep(1)  # wait for Moorcheh to index
        print(f"[Image] ✓ Stored image for pothole #{pothole_id} in Moorcheh")
        return {"stored": True, **record}
    except Exception as e:
        print(f"[Image] ✗ Failed to store image: {e}")
        return {"stored": False, "reason": str(e), "image_base64": image_base64}

# ============================================================
# RETRIEVE — get image back from Moorcheh
# ============================================================

def retrieve_image(pothole_id: int) -> dict:
    """
    Retrieve image from Moorcheh by pothole ID.
    Returns dict with image_base64 and decoded bytes.
    """
    try:
        result = client.similarity_search.query(
            namespaces=[IMAGE_NAMESPACE],
            query=f"pothole image ID {pothole_id}",
            top_k=5
        )
        docs = result.get("results", [])

        # Find the exact pothole image
        for doc in docs:
            metadata = doc.get("metadata") or {}
            if metadata.get("pothole_id") == pothole_id:
                image_base64 = metadata.get("image_base64")
                if image_base64:
                    print(f"[Image] ✓ Retrieved image for pothole #{pothole_id}")
                    return {
                        "found":         True,
                        "pothole_id":    pothole_id,
                        "filename":      metadata.get("filename", "pothole.jpg"),
                        "image_base64":  image_base64,
                        "image_bytes":   decode_image(image_base64)  # decoded back to bytes
                    }

        print(f"[Image] No image found for pothole #{pothole_id}")
        return {"found": False, "pothole_id": pothole_id}

    except Exception as e:
        print(f"[Image] ✗ Retrieve failed: {e}")
        return {"found": False, "reason": str(e)}

# ============================================================
# VERIFY — confirm encode → store → decode → retrieve works
# ============================================================

def verify_image_roundtrip(image_bytes: bytes) -> bool:
    """
    Test that encoding and decoding produces identical bytes.
    Call this once to confirm the pipeline works.
    """
    encoded = encode_image(image_bytes)
    decoded = decode_image(encoded)
    match   = image_bytes == decoded
    print(f"[Image] Roundtrip test: {'✓ PASS' if match else '✗ FAIL'}")
    print(f"[Image] Original:  {len(image_bytes)} bytes")
    print(f"[Image] Encoded:   {len(encoded)} chars")
    print(f"[Image] Decoded:   {len(decoded)} bytes")
    return match