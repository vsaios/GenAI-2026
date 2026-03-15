import os
from dotenv import load_dotenv
from moorcheh_sdk import MoorchehClient
from moorcheh_sdk.exceptions import ConflictError

load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '.env')))

client = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))

# Namespace 1 — pothole records (already exists)
try:
    client.namespaces.create(namespace_name="toronto_potholes", type="text")
    print("✓ toronto_potholes namespace created")
except ConflictError:
    print("✓ toronto_potholes namespace already exists")

# Namespace 2 — image storage (NEW)
try:
    client.namespaces.create(namespace_name="pothole_images", type="text")
    print("✓ pothole_images namespace created")
except ConflictError:
    print("✓ pothole_images namespace already exists")

print("\n✓ Both namespaces ready")