# Rua — Mapping what matters

**Rua** is an AI-powered infrastructure monitoring web app that detects, maps, and prioritizes potholes and road hazards. Users land on a home page with a world view and value proposition, then sign up or log in (Supabase). After auth, a dashboard shows a 3D Mapbox map of incidents with orange hotspots, addresses, and severity. A Toronto-focused map view and an AI chat assistant answer questions about road safety and can drive map navigation; the backend uses an LLM with Moorcheh SDK memory for replies and optional 311 email reports. Users can submit incidents (location, type, severity, optional photo/email); reports are stored in SQLite and shown as clusters and popups, with user submissions as distinct markers. Stack: one `requirements.txt` for backend + AI, React + Vite frontend, single FastAPI backend for maps, auth, reports, chat, and AI.

---

## How to run the project

### Prerequisites

- **Python 3.10+** (for backend and AI)
- **Node.js 18+** and **npm** (for frontend)
- **Supabase** project (for auth; get URL and anon key from dashboard)
- **Mapbox** access token (optional but recommended for the 3D map)

### 1. Backend and AI (port 8000)

From the repo root, backend and AI share the same Python dependencies.

```bash
cd pothole-ai-system
pip install -r requirements.txt
```

If you use a **virtual environment** in `backend/` (e.g. `backend/venv`), install there and run with that interpreter:

```bash
cd pothole-ai-system/backend
# Create venv if needed: python -m venv venv
# Windows:
venv\Scripts\pip install -r ..\requirements.txt
# Then run (Windows PowerShell):
$env:PYTHONPATH = "C:\path\to\pothole-ai-system\ai\Moorcheh"
venv\Scripts\uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000
# Linux/macOS:
PYTHONPATH="../ai/Moorcheh" .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **PYTHONPATH** must point to `ai/Moorcheh` so the app can import `memory_client`, `report_generator`, etc.
- Backend **.env** (in `backend/`): add any keys your backend needs (e.g. Moorcheh, OpenAI, Resend). See `backend/.env.example` if present.
- **Optional:** Seed the Moorcheh memory so the map has incident data (run from `ai/Moorcheh` with UTF-8 for emoji):  
  `PYTHONUTF8=1 python seed_demo.py` then `seed_fix.py` / `seed_fixshoe.py` as needed.

### 2. Frontend (port 5173)

```bash
cd pothole-ai-system/frontend
npm install
```

Copy `frontend/.env.example` to `frontend/.env` and set:

- **VITE_SUPABASE_URL** — Supabase project URL
- **VITE_SUPABASE_ANON_KEY** — Supabase anon/public key
- **VITE_MAPBOX_TOKEN** — (optional) Mapbox token for the 3D map; without it the map may not show tiles or points correctly.

Then:

```bash
npm run dev
```

Vite runs at **http://localhost:5173** and proxies `/api`, `/chat`, `/api/reports`, etc. to **http://localhost:8000**. The backend must be running for reports, chat, and map data.

### 3. Using the app

1. Open **http://localhost:5173**.
2. Use **Sign up** / **Log in** (Supabase).
3. **Dashboard** and **Toronto Map** show incidents from the backend; if you see no dots, ensure the backend is up and (if applicable) seed scripts have been run.
4. Use the **Report** flow to submit an incident; use the **chat** to ask about road safety and trigger map navigation.

---

## Product overview 

- **Inspiration** — Toronto’s roads are under stress and reporting is manual and reactive. We wanted an autonomous system that “sees” the city’s needs in real time and turns detections into actionable reports.
- **What it does** — End-to-end road monitoring: **detection** (e.g. YOLOv8 on dashcam), **intelligence** (GPS, street, severity logged in Moorcheh), **action** (AI-generated 311 reports via email), **visualization** (3D Mapbox heatmap), **interaction** (AI chatbot over the live database).
- **How we built it** — Computer vision (YOLOv8), FastAPI backend, React + Mapbox GL JS frontend, Moorcheh for memory, LLM (e.g. Hugging Face) for reports and chat, optional hardware/dashcam integration.
- **Challenges** — Avoiding duplicate 311 reports: we used spatial clustering in Moorcheh so multiple sightings of the same defect become one verified incident.
- **What we learned** — GenAI’s power here is as a bridge between raw sensory data and civic action.
- **What’s next** — Scale via ride-share and transit fleets to turn existing vehicles into a “digital nervous system” toward Vision Zero for Toronto’s streets.
