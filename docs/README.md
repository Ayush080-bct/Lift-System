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

#### Lifts Management
- `GET /lifts` - Get all lifts (current state)
- `GET /lifts/{lift_id}` - Get specific lift status
- `PUT /lifts/{lift_id}` - Update lift floor/direction/door_status

#### Requests (Floor Requests)
- `POST /requests?floor=X&lift_id=Y` - Create new floor request (auto-assigned to lift)
- `GET /requests` - Get all pending requests
- `PUT /requests/{request_id}` - Mark request as served

#### Event Logs
- `POST /logs` - Add event log
- `GET /logs` - Get all event logs (shows last 20 in frontend)

#### Scheduling (SCAN Algorithm)
- `GET /next_floor/{lift_id}` - Get next floor for lift to visit
- `POST /simulate_lift_step/{lift_id}` - Execute one lift movement step (called by background scheduler)

---

## SCAN Algorithm

### What is SCAN?

SCAN (Elevator Scheduling) algorithm determines the **OPTIMAL ORDER OF STOPS** for a single lift when it has multiple floor requests.

**Key Concept:**
- Lift moves in ONE direction (up/down) serving all requests in that direction
- Once no more requests exist in current direction, lift REVERSES direction
- This minimizes total travel time and energy

### How It Works

```
For ONE lift with multiple requests:

Step 1: Get all pending requests for this lift
Step 2: Determine next floor in current direction
Step 3: Move to that floor
Step 4: If requests exist in current direction → go to Step 2
Step 5: If NO requests in current direction → reverse direction
Step 6: Repeat from Step 2 in new direction
```

### Example

```
Lift Position: Floor 5, Direction: UP
Pending Requests: [3, 7, 10]

Current: Floor 5, Direction: UP
→ Floors ABOVE (in UP direction): [7, 10]
→ Next floor: 7 (closest ahead)
→ Move to 7, serve request
→ Current: Floor 7, Direction: UP

Current: Floor 7, Direction: UP
→ Floors ABOVE: [10]
→ Next floor: 10
→ Move to 10, serve request
→ Current: Floor 10, Direction: UP

Current: Floor 10, Direction: UP
→ Floors ABOVE: [] (empty)
→ No more requests going UP, REVERSE direction

Current: Floor 10, Direction: DOWN
→ Floors BELOW: [3]
→ Next floor: 3
→ Move to 3, serve request
→ DONE! All requests served
```

### Implementation in Code

```python
def get_next_floor_for_lift(self, lift_id: int):
    """
    Returns next floor to visit for this lift using SCAN logic
    """
    lift = self.repo.get_lift(lift_id)  # Current state
    pending_requests = self.repo.get_pending_request()
    
    # Get floors for this lift only
    lift_requests = [req for req in pending_requests if req.lift_id == lift_id]
    
    if not lift_requests:
        return None  # No requests, stay idle
    
    floors = sorted(set(req.floor for req in lift_requests))
    current_floor = lift.current_floor
    
    # SCAN: Continue in current direction
    if lift.direction == "up":
        floors_above = [f for f in floors if f > current_floor]
        if floors_above:
            return min(floors_above)  # Go to closest floor above
        else:
            # No floors above, must go down
            return max(floors)  # Go to top floor first, then down
    
    elif lift.direction == "down":
        floors_below = [f for f in floors if f < current_floor]
        if floors_below:
            return max(floors_below)  # Go to closest floor below
        else:
            # No floors below, must go up
            return min(floors)  # Go to bottom floor first, then up
```

### Why SCAN is Optimal

✅ **Minimizes travel time** - No back-and-forth between floors  
✅ **Fair service** - All requests in direction served before reversing  
✅ **Energy efficient** - Continuous motion in one direction  
✅ **User friendly** - Predictable behavior

---

## Data Flow

### Request Lifecycle

```
1. User enters lift and presses "Floor 5" button
   ↓
2. Frontend: RequestPanel → createRequest(floor=5, lift_id=1)
   ↓
3. Backend: POST /requests?floor=5&lift_id=1
   ↓
4. Repository: INSERT into requests table (lift_id already assigned)
   ↓
5. Repository: INSERT into logs ("Request 10 created for floor 5")
   ↓
6. Frontend: Fetches /requests (polling every 3s)
   ↓
7. RequestQueue displays: Request 10, Floor 5, Lift 1, Status=pending
   ↓
8. Backend: Background scheduler triggers simulate_lift_step(1)
   ↓
9. SCAN algorithm: get_next_floor_for_lift(1) → Returns floor 5
   ↓
10. Lift moves one floor toward floor 5
    ↓
11. Repository: UPDATE lifts SET current_floor=2, direction=UP
    ↓
12. Repository: INSERT into logs ("Moved UP to floor 2")
    ↓
13. Frontend: Fetches /lifts (polling every 3s) → Shows lift at floor 2
    ↓
14. [Steps 8-13 repeat until lift reaches floor 5]
    ↓
15. Lift arrives at floor 5
    ↓
16. update_and_serve(): Open doors, mark request as served, close doors
    ↓
17. Repository: DELETE from requests (request served)
    ↓
18. Repository: INSERT into logs ("Served request 10 at floor 5")
    ↓
19. LogViewer displays event
    ↓
20. Dashboard shows: No pending requests, Lift 1 idle at floor 5
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
