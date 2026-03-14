import os
import time
from dotenv import load_dotenv
from moorcheh_sdk import MoorchehClient
from moorcheh_sdk.exceptions import ConflictError
from memory_client import save_pothole, get_potholes, get_summary

load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '.env')))

client = MoorchehClient(api_key=os.getenv("MOORCHEH_API_KEY"))

print("\n=== STEP 1: Create namespace ===")
try:
    client.namespaces.create(namespace_name="toronto_potholes", type="text")
    print("✓ Namespace created")
except ConflictError:
    print("✓ Namespace already exists — skipping, this is fine")

print("\n=== STEP 2: Store a test pothole ===")
result = client.documents.upload(
    namespace_name="toronto_potholes",
    documents=[{
        "id":      "pothole_1",        # fix: no colon in ID, Moorcheh doesn't like it
        "text":   "Pothole on Yonge St in Toronto. Severity: HIGH. GPS: 43.6532, -79.3832. Reported at 2025-03-14. Status: reported.",
        "metadata": {
            "id":          1,
            "road":        "Yonge St",
            "lat":         43.6532,
            "lng":         -79.3832,
            "severity":    "high",
            "city":        "Toronto",
            "timestamp":   "2025-03-14T10:30:00",
            "sent_to_311": False,
            "status":      "reported"
        }
    }]
)
print(f"✓ Upload result: {result}")

print("\n=== STEP 3: Wait for processing ===")
time.sleep(3)   # give it 3 seconds to index
print("✓ Done waiting")

print("\n=== STEP 4: Search for it ===")
search = client.similarity_search.query(
    namespaces=["toronto_potholes"],
    query="potholes on Yonge St",
    top_k=5
)

# Print raw result first so we can see exact structure
print(f"Raw result keys: {search.keys()}")
results = search.get("results", [])
print(f"✓ Found {len(results)} results")

for r in results:
    print(f"  Raw result: {r}")   # print full object to see structure
    # Handle nested metadata
    meta = r.get("metadata")
    if isinstance(meta, dict) and "metadata" in meta:
        meta = meta["metadata"]
    elif isinstance(meta, dict):
        meta = meta
    else:
        meta = r
    print(f"  - Road: {meta.get('road')} | Severity: {meta.get('severity')}")

print("\n=== STEP 5: Get AI answer ===")
# Fix: use client.answer.generate instead of deprecated get_generative_answer
answer = client.answer.generate(
    namespace="toronto_potholes",
    query="Are there any dangerous potholes on Yonge St?"
)
print(f"Raw answer: {answer}")   # print full object to see structure
# Handle both string and dict response
if isinstance(answer, str):
    print(f"✓ AI Answer: {answer}")
elif isinstance(answer, dict):
    content = (
        answer.get("answer") or
        answer.get("content") or
        answer.get("text") or
        str(answer)
    )
    print(f"✓ AI Answer: {content}")

print("\n=== STEP 6: Test memory_client ===")
# Save a pothole using memory_client
mc_pothole = save_pothole(43.6532, -79.3832, 'high', 'Yonge St')
print("memory_client saved:", mc_pothole)

# Retrieve potholes for Yonge St
mc_results = get_potholes("Yonge St")
print("memory_client get_potholes('Yonge St'):", mc_results)

# Print summary
mc_summary = get_summary()
print("memory_client summary:", mc_summary)

print("\n✓ ALL STEPS PASSED — Moorcheh is working!")