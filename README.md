# Lift Control System

Full-stack elevator simulation: FastAPI + PostgreSQL backend, React + TypeScript frontend.  
Uses the **SCAN** scheduling algorithm. Phase 1 runs **one lift** (floors 1–10); the backend can handle more lifts when you add rows to the database.

## What it does

- **Hall calls** — UP/DOWN buttons at each floor (outside panel)
- **Inside lift** — floor buttons 1–10 to pick a destination
- **Automatic movement** — backend moves the lift every 2 seconds (open doors, serve requests, move one floor)
- **SCAN ordering** — serves stops in one direction, then reverses (e.g. at floor 1 going up: 5 → 6 → 8)
- **Dashboard** — lift status, pending requests, event logs (polling)

## Tech stack

| Layer | Stack |
|-------|--------|
| Backend | Python, FastAPI, psycopg2, python-dotenv |
| Database | PostgreSQL (connection pool) |
| Frontend | React, TypeScript, Vite |

## Project structure

```
LiftSystem/
├── backend/
│   ├── app/main.py              # REST API + background simulation
│   ├── database/Schema.sql      # tables + seed (lift 1)
│   ├── model/                   # dataclasses + DB pool
│   ├── repository/              # SQL access
│   └── service/                 # SCAN scheduling
├── frontend/
│   └── src/
│       ├── pages/ControlPage    # shaft + hall + inside panel
│       ├── pages/DashboardPage  # status tables
│       └── services/api.ts      # API client
├── .env.example
└── QUICKSTART.md                # step-by-step run guide
```

## Quick start

See **[QUICKSTART.md](QUICKSTART.md)** for full steps. Short version:

```bash
# 1. Database
cp .env.example .env          # set DB_PASS
psql -U ayush -d lift_system -f backend/database/Schema.sql

# 2. Backend (from project root)
source Lvenv/bin/activate
fastapi dev backend/app/main.py

# 3. Frontend
cd frontend && npm install && npm run dev
```

- Control UI: http://localhost:5173/
- API: http://127.0.0.1:8000/
- Dashboard: http://localhost:5173/dashboard

## Environment variables

Create `.env` in the project root (see `.env.example`):

```
DB_NAME=lift_system
DB_USER=ayush
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Frontend pages

### Control (`/`)

- One animated lift shaft (car moves with CSS; doors open/close)
- Hall call column — ▲/▼ per floor
- Inside panel — destination buttons
- Pending requests table

When you add more lifts later, use the lift chips to switch which one is shown in the shaft (others appear as cards on the dashboard).

### Dashboard (`/dashboard`)

- All lifts (floor, direction, doors)
- Pending requests
- Last 20 event logs

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/lifts` | All lifts |
| GET | `/lifts/{id}` | One lift (full status) |
| PUT | `/lifts/{id}` | Update lift (`floor`, `direction`, `door_status` query params) |
| POST | `/requests?floor=5` | New request (auto-assigns best lift) |
| GET | `/requests` | Pending requests |
| PUT | `/requests/{id}` | Mark request served |
| GET | `/logs` | Event logs (newest first, limit 50) |
| POST | `/logs` | Add log (`lift_id`, `event_type`) |
| GET | `/next_floor/{id}` | Next stop + SCAN queue |
| POST | `/simulate_lift_step/{id}` | Manual one-step simulation (optional) |

**Log event types:** `button_pressed`, `lift_arrived`, `door_opened`, `door_closed`, `emergency_stop`

Floors must be between **1** and **10**.

## Architecture

```
React UI  →  REST API (main.py)  →  SchedulingService (SCAN)
                                      ↓
                               LiftRepository  →  PostgreSQL
```

1. **Model** (`backend/model/`) — `Lift`, `Request`, `Log` dataclasses; connection pool  
2. **Repository** (`backend/repository/`) — all SQL  
3. **Service** (`backend/service/`) — assign lift, next floor, `update_and_serve`  
4. **API** (`backend/app/`) — async routes; background task moves lifts every 2s  

Simulation runs on the **backend only**. The frontend polls every 2s to refresh the UI.

## SCAN algorithm (short)

1. New request → `assign_lift_to_request()` picks the best lift (moving toward floor, closest idle, or nearest; skips lifts with more than 5 pending jobs).
2. Each tick → serve requests at current floor (doors open → mark served → doors close).
3. Move one floor toward the next stop in SCAN order (up: lowest floor above; then reverse down).

Example: at floor 1, going up, requests for 5, 6, 8 → order **5 → 6 → 8**.

## Database tables

| Table | Purpose |
|-------|---------|
| `lifts` | `lift_id`, `current_floor`, `direction`, `door_status` |
| `requests` | `floor`, `status` (pending/served), `lift_id` |
| `logs` | `lift_id`, `event_type`, `event_time` |

Reset data (dev only): see `backend/database/Queries.sql`.

## Scaling to multiple lifts

1. Insert another row: `INSERT INTO lifts (current_floor, direction, door_status) VALUES (1, 'idle', 'closed');`
2. POST `/requests` already assigns via SCAN across all lifts.
3. Control page shows a chip per lift to switch the animated shaft.

## Troubleshooting

| Problem | Check |
|---------|--------|
| `Failed to fetch` in UI | Backend on :8000, CORS, `.env` / Postgres up |
| `DB_PASS not found` | `.env` in project root |
| Lift not moving | Backend logs; simulation runs in lifespan task |
| Log insert fails | `event_type` must be one of the five allowed values |

## Docs

- [QUICKSTART.md](QUICKSTART.md) — run locally  
- [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) — detailed design notes  
- [docs/README.md](docs/README.md) — extra architecture write-up  

## Author notes

Built as a 3rd-year style project: plain CSS, repository pattern, SCAN elevator logic, and real-time polling instead of WebSockets.
