# Lift System Architecture Documentation

## 📚 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Frontend Architecture](#frontend-architecture)
4. [Backend Architecture](#backend-architecture)
5. [SCAN Algorithm](#scan-algorithm)
6. [Data Flow](#data-flow)
7. [Component Diagram](#component-diagram)

---

## Project Overview

**Lift System** is a full-stack application that simulates a real-time elevator management system. It demonstrates:
- Database design and optimization
- RESTful API development
- Scheduling algorithms
- Frontend-backend integration
- Real-time state management

**Tech Stack:**
- **Frontend:** React + TypeScript + Vite
- **Backend:** FastAPI + Python
- **Database:** PostgreSQL
- **Architecture:** Layered (Repository → Service → API)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    LIFT SYSTEM                              │
├──────────────────────┬──────────────────────────────────────┤
│      FRONTEND        │         BACKEND                      │
│  (React + TypeScript)│   (FastAPI + Python)                │
│                      │                                      │
│  ┌────────────────┐  │  ┌──────────────────┐               │
│  │  LiftsList     │  │  │  API Endpoints   │               │
│  │  RequestPanel  │  │  │  (main.py)       │               │
│  │  RequestQueue  │  │  └──────────────────┘               │
│  │  LogViewer     │  │           ↓                         │
│  └────────────────┘  │  ┌──────────────────┐               │
│         ↓            │  │  Service Layer   │               │
│  ┌────────────────┐  │  │ (SCAN algorithm) │               │
│  │   API Service  │  │  └──────────────────┘               │
│  │   (api.ts)     │  │           ↓                         │
│  └────────────────┘  │  ┌──────────────────┐               │
│         ↓            │  │ Repository Layer │               │
│  ┌────────────────┐  │  │  (DB operations) │               │
│  │   State Mgmt   │  │  └──────────────────┘               │
│  │  (useState)    │  │           ↓                         │
│  └────────────────┘  │  ┌──────────────────┐               │
│         ↓            │  │   PostgreSQL     │               │
│    [Display]         │  │     Database     │               │
│                      │  └──────────────────┘               │
└──────────────────────┴──────────────────────────────────────┘
         HTTP API (REST)
```

---

## Frontend Architecture

### Folder Structure
```
frontend/src/
├── components/
│   ├── LiftCard.tsx           # Single lift display card
│   ├── LiftsList.tsx          # Grid of all lifts
│   ├── RequestPanel.tsx       # Form to request lift
│   ├── RequestQueue.tsx       # Pending requests table
│   ├── LogViewer.tsx          # Event logs table
│   └── styles/
│       ├── LiftCard.css
│       ├── LiftsList.css
│       ├── RequestPanel.css
│       ├── RequestQueue.css
│       └── LogViewer.css
├── services/
│   └── api.ts                 # API calls (fetch data)
├── types/
│   └── index.ts               # TypeScript interfaces
├── App.tsx                    # Main app component
├── App.css                    # Main layout (6:3:1 grid)
└── main.tsx                   # Entry point
```

### Component Hierarchy

```
App
├── Header (Title + Subtitle)
└── Layout (6:3:1 Grid)
    ├── Main (6fr width)
    │   └── LiftsList
    │       └── LiftCard × N
    ├── Sidebar (3fr width)
    │   ├── RequestPanel
    │   └── RequestQueue
    └── Full Width
        └── LogViewer
```

### Data Flow

```
Component → useEffect (on mount) → API Service → Fetch → State (setState)
                                                   ↓
                                            Backend Response
                                                   ↓
                                           Render/Display
```

### Key Components

| Component | Purpose | State | API Call |
|-----------|---------|-------|----------|
| `LiftsList` | Display all lifts | `lifts[]` | `getAllLifts()` |
| `LiftCard` | Show single lift | Props only | None |
| `RequestPanel` | Create requests | `floor`, `loading` | `createRequest()` |
| `RequestQueue` | Show pending requests | `requests[]` | `getRequests()` |
| `LogViewer` | Display event logs | `logs[]` | `getLogs()` |

---

## Backend Architecture

### Layered Architecture Pattern

```
┌────────────────────────────────────┐
│      API Layer (main.py)           │
│  (/lifts, /requests, /logs)        │
└────────────────┬───────────────────┘
                 ↓
┌────────────────────────────────────┐
│    Service Layer (SCAN Algorithm)  │
│  (assign_lift_to_request)          │
│  (get_next_floor_for_lift)         │
└────────────────┬───────────────────┘
                 ↓
┌────────────────────────────────────┐
│   Repository Layer (DB Operations) │
│  (get_lift, add_request, etc.)     │
└────────────────┬───────────────────┘
                 ↓
┌────────────────────────────────────┐
│       PostgreSQL Database          │
│  (lifts, requests, logs tables)    │
└────────────────────────────────────┘
```

### Folder Structure
```
backend/
├── app/
│   └── main.py              # FastAPI endpoints
├── model/
│   ├── models.py            # Data classes (Lift, Request, Log)
│   └── databases.py         # DB connection
├── repository/
│   └── repository.py        # Database CRUD operations
├── service/
│   └── scheduling_service.py # SCAN algorithm logic
└── database/
    ├── Schema.sql           # Table structure
    └── Queries.sql          # Common queries
```

### API Endpoints

#### Lifts
- `GET /lifts` - Get all lifts
- `GET /lifts/{lift_id}` - Get specific lift
- `PUT /lifts/{lift_id}` - Update lift position

#### Requests
- `POST /requests?floor=X` - Create new request
- `GET /requests` - Get all pending requests
- `PUT /requests/{request_id}` - Mark as served

#### Logs
- `POST /logs?lift_id=X&event_type=Y` - Add event log
- `GET /logs` - Get all logs

#### Scheduling
- `POST /assign_lift/{request_id}` - Auto-assign lift (SCAN)
- `GET /next_floor/{lift_id}` - Get next floor to visit

---

## SCAN Algorithm

### What is SCAN?

SCAN (Elevator Scheduling) algorithm moves lifts in one direction until all requests are served, then reverses direction.

### How It Works

```
Step 1: Check lift's current direction (up/down/idle)
Step 2: Find all pending requests for this lift
Step 3: Get next unserved floor in current direction
Step 4: If no floors ahead, reverse and go opposite direction
Step 5: Move lift and repeat
```

### Example

```
Lift at floor 5, moving UP
Pending requests: [3, 7, 10]

Current: 5, Direction: UP
→ Next floor above: 7 ✓ (serve)
→ Current: 7, Direction: UP
→ Next floor above: 10 ✓ (serve)
→ Current: 10, Direction: UP
→ No floors above, reverse to DOWN
→ Next floor below: 3 ✓ (serve)
→ Current: 3, Direction: DOWN
→ Done!
```

### Implementation

```python
def assign_lift_to_request(self, requested_floor: int):
    # 1. Get all lifts
    # 2. Count pending requests per lift
    # 3. Score each lift based on:
    #    - Distance to requested floor
    #    - Current load (penalty: load × 2)
    #    - Direction match (prefer lifts already moving toward floor)
    # 4. Return lift with lowest score
```

---

## Data Flow

### Request Lifecycle

```
1. User clicks "Request Lift" at Floor 5
   ↓
2. Frontend: RequestPanel → createRequest(5)
   ↓
3. Backend: POST /requests?floor=5
   ↓
4. Repository: INSERT into requests table
   ↓
5. Frontend: Fetches /requests (pollng every 2s)
   ↓
6. RequestQueue displays new request
   ↓
7. User/System: POST /assign_lift/{request_id}
   ↓
8. Backend: Service → SCAN algorithm → Pick best lift
   ↓
9. Repository: UPDATE requests SET lift_id = X
   ↓
10. Repository: INSERT into logs (auto-logging)
   ↓
11. Frontend: Displays assigned lift in RequestQueue
    ↓
12. Lift moves and serves request
    ↓
13. PUT /requests/{request_id} → Mark as served
    ↓
14. LogViewer shows event
```

### Real-Time Updates

Frontend uses **polling** (every 2 seconds):
```typescript
useEffect(() => {
  const interval = setInterval(() => {
    fetchData();  // Refresh lifts, requests, logs
  }, 2000);
  return () => clearInterval(interval);
}, []);
```

---

## Component Diagram

### Frontend Components

```
                        App
                    (Layout 6:3:1)
                        |
            ┌───────────┼───────────┐
            |           |           |
        Header      LiftsList   RequestPanel
                      |        RequestQueue
                    LiftCard       |
                      ×N        LogViewer
```

### Backend Layers

```
                      Client
                        ↓
                  [API Endpoints]
                     /lifts
                    /requests
                      /logs
                        ↓
                 [Service Layer]
           SchedulingService (SCAN)
                        ↓
                [Repository Layer]
            LiftRepository (CRUD ops)
                        ↓
                   PostgreSQL DB
```

---

## Database Schema

### Tables

**lifts**
- `lift_id` (PK)
- `current_floor`
- `direction` (up/down/idle)
- `door_status` (open/closed)

**requests**
- `request_id` (PK)
- `floor`
- `request_time`
- `status` (pending/served)
- `lift_id` (FK)

**logs**
- `log_id` (PK)
- `lift_id` (FK)
- `event_type`
- `event_time`

---

## Key Design Patterns

### 1. Repository Pattern
Separates data access from business logic
```
Controller → Service → Repository → Database
```

### 2. Component Isolation
Each component manages its own state and CSS
```
LiftCard.tsx imports LiftCard.css
RequestPanel.tsx imports RequestPanel.css
```

### 3. API Service Layer
Centralized API calls in `api.ts`
```
Components → API Service → Backend
```

### 4. Type Safety
TypeScript interfaces for all data structures
```typescript
interface Lift { ... }
interface Request { ... }
```

---

## Performance Considerations

1. **Polling Interval:** 2 seconds (balance between freshness and server load)
2. **Load Limiting:** Max 5 pending requests per lift
3. **Query Optimization:** Index on frequently searched fields
4. **Component Memoization:** Could use `React.memo()` for LiftCard
5. **Lazy Loading:** Could implement for large log lists

---

## Future Enhancements

- [ ] WebSocket for real-time updates (vs polling)
- [ ] User authentication & authorization
- [ ] Multiple buildings/floors
- [ ] Predictive algorithms (ML-based)
- [ ] Mobile app
- [ ] Maintenance schedules
- [ ] Energy optimization
- [ ] Analytics dashboard

---

**Last Updated:** May 21, 2026
