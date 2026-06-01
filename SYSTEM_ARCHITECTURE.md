# LIFT SYSTEM - Complete Architecture & Implementation Guide

## 📋 SYSTEM OVERVIEW

You're building a **10-Floor Lift Management System** with:
- **Backend**: FastAPI (REST API) + PostgreSQL Database
- **Frontend**: React + TypeScript (Vite)
- **Algorithm**: SCAN Algorithm for optimal stop ordering (ONE lift)
- **Data Flow**: Real-time via polling (3 seconds)
- **Current Phase**: Single Lift (lift_id=1) - Scales to multiple lifts later

---

## 🏗️ ARCHITECTURE LAYERS

### Layer 1: DATABASE (PostgreSQL)
Tables needed:
- `lifts` - Current state of each lift (floor, direction, door status) - **ONE row for now**
- `requests` - User requests (floor, status: pending/served, lift_id)
- `logs` - Event history (button pressed, door opened, lift arrived, etc.)

### Layer 2: BACKEND (FastAPI)
**Three Main Services:**

1. **LiftRepository** - Database queries
   - Get lift status
   - Update lift position/direction
   - Mark requests as served
   - Log events

2. **SchedulingService** - SCAN Algorithm
   - When request created → **Automatically assign to lift_id=1**
   - Find next floor for lift using SCAN
   - Determine optimal order of stops

3. **REST API** - Endpoints
   - GET `/lifts` - All lifts current status
   - GET `/requests` - All pending requests
   - GET `/logs` - All events
   - POST `/requests?floor=3&lift_id=1` - Create new request (auto-assigned)
   - PUT `/requests/{id}` - Mark as served
   - GET `/next_floor/{lift_id}` - Get next floor for lift (SCAN)
   - POST `/simulate_lift_step/{lift_id}` - Move lift one step (called by background scheduler)

### Layer 3: FRONTEND (React)

**Two Main Pages:**

1. **Control Page (`/`)**
   - **Left**: Visual lift shaft with animated lift (floors 1-10)
   - **Left**: Outside buttons (⬆️ UP / ⬇️ DOWN - for future multiple lifts)
   - **Right**: Inside lift buttons (floors 1-10)
   - **Right**: Display pending requests
   - Auto-updates lift position every 3 seconds

2. **Dashboard Page (`/dashboard`)**
   - **Lifts Section**: Real-time lift status (floor, direction, door)
   - **Requests Section**: Pending/served requests
   - **Logs Section**: Event history
   - **Polling**: Every 3 seconds fetches fresh data

---

## 🔄 DATA FLOW (User's Perspective)

### Scenario: User Inside Lift Presses Floor 5 Button

```
1. USER ACTION (Frontend)
   User presses "Floor 5" button inside lift
   ↓
2. FRONTEND → BACKEND
   POST /requests?floor=5&lift_id=1
   ↓
3. BACKEND Processing
   a) Save request to DB (floor: 5, lift_id: 1, status: "pending")
   b) Create log: "Request created for floor 5"
   ↓
4. BACKGROUND SCHEDULER (Automatic)
   - Every 2 seconds triggers: POST /simulate_lift_step/1
   - SCAN algorithm: Get next floor for lift 1
   - Move lift one floor closer
   - Update DB: lifts.current_floor
   - Create log: "Moved UP to floor X"
   - When lift reaches floor 5:
     * Open doors, mark request as served
     * Create log: "Served request at floor 5"
   ↓
5. FRONTEND POLLING (Every 3 seconds)
   GET /lifts, GET /requests, GET /logs
   ↓
6. DASHBOARD UPDATES AUTOMATICALLY
   - Shows: "Lift 1 at Floor 5"
   - Shows: Request #5 → "Served"
   - Shows: New logs of events
```

---

## 🎯 WHAT NEEDS TO BE BUILT

### Frontend Features

#### Control Page (/)
- **Left Side: Lift Visualization + Outside Buttons**
  - 10 floors displayed (F10, F9, F8...F1)
  - Animated lift box moving between floors
  - Show: Current floor, direction (↑↓), door status (open/closed)
  - Outside buttons: ⬆️ UP / ⬇️ DOWN (for multiple lifts - disabled for now)

- **Right Side: Inside Panel + Request Queue**
  - Buttons for each floor (1-10) - What person presses inside lift
  - When pressed → Create request with lift_id=1
  - Show feedback: "Floor 5 requested"
  - Show pending requests table below

#### Dashboard Page (/dashboard)
- **Section 1: Lift Status**
  - Current floor, direction, door status
  - Updates every 3 seconds

- **Section 2: Request Queue**
  - Pending requests (awaiting lift arrival)
  - Show: Request ID, Floor, Status

- **Section 3: Event Logs**
  - Real-time list of all events
  - Latest 20 events shown
  - Auto-scrolling

### Backend Features
- ✅ Lift endpoints (GET, PUT)
- ✅ Request endpoints (POST, GET, PUT)
- ✅ Log endpoints (GET, POST)
- ✅ SCAN algorithm for stop ordering
- ✅ Auto-assign to lift_id=1 during request creation
- ✅ Background scheduler (lifespan) for automatic lift movement

---

## 🔌 POLLING MECHANISM

**Frontend Side:**
```
When Page loads:
1. Fetch initial data (lifts, requests, logs)
2. Set interval: Every 3 seconds
3. Call: GET /lifts, GET /requests, GET /logs
4. Update React state
5. Re-render UI with new data
```

**Why Polling?**
- Simple to implement
- Works for single lift system
- Frontend always sees current state
- No WebSocket complexity (yet)

---

## 🧠 SCAN ALGORITHM EXPLAINED

### What it does:
For ONE lift, determines the **OPTIMAL ORDER OF STOPS** to serve all pending requests efficiently.

### Key Concept:
SCAN does NOT choose which lift - it determines which FLOOR to visit next.

### Example:
```
Current: Lift at Floor 3, direction = UP
Pending requests: Floors [2, 5, 7, 1]

SCAN Logic:
1. Current direction UP → Visit floors ABOVE first
   - Next floor above: 5 (closest)
   - Serve floor 5
2. Next floor above: 7
   - Serve floor 7
3. No more floors above → REVERSE to DOWN
4. Next floor below: 2
   - Serve floor 2
5. Next floor below: 1
   - Serve floor 1
6. Done! All requests served.

Order served: 5 → 7 → 2 → 1 (Optimal path!)
```

### Benefits:
- ✅ Minimizes total travel distance
- ✅ No back-and-forth between floors
- ✅ Efficient for single lift

---

## 📊 STATE MANAGEMENT

### What Data Lives Where?

**Backend (Database) - Source of Truth**
```
lifts: 
  - lift_id=1, current_floor=3, direction=UP, door_status=closed

requests: 
  - request_id=10, floor=5, lift_id=1, status=pending
  - request_id=11, floor=7, lift_id=1, status=pending

logs: 
  - "Request 10 created for floor 5"
  - "Lift 1 moved UP to floor 4"
  - "Lift 1 arrived at floor 5"
```

**Frontend (React State) - Temporary Copy**
```
ControlPage:
  - lift: {floor: 3, direction: UP, door_status: closed}
  - requests: [{request_id: 10, floor: 5}, ...]

DashboardPage:
  - lift: {floor: 3, direction: UP, door_status: closed}
  - requests: [...]
  - logs: [...]
```

---

## 🎬 IMPLEMENTATION STEPS

### Phase 1: Setup (Already Done)
- ✅ React Router (2 pages: Control, Dashboard)
- ✅ API service (fetch functions)
- ✅ Basic component structure

### Phase 2: Control Page - Build UI
1. Create lift visualization with 10 floors
2. Create inside lift floor buttons (1-10)
3. Create outside buttons (UP/DOWN)
4. Display requests table

### Phase 3: Request System
1. When user clicks floor → Create request
2. Backend auto-assigns to lift_id=1
3. Display in UI

### Phase 4: Automatic Movement
1. Background scheduler moves lift every 2 seconds
2. SCAN algorithm determines next floor
3. Lift animates to next floor

### Phase 5: Dashboard - Real-time Display
1. Setup polling (every 3 seconds)
2. Show lift current status
3. Show requests (pending + served)
4. Show events

---

## 📱 UI/UX FLOW

### User Opens App
```
App loads on Control Page (/)
  ↓
Shows 10-floor building with animated lift at floor 1
  ↓
User inside lift clicks "Floor 5" button
  ↓
Request created (auto-assigned to lift_id=1)
  ↓
Background scheduler starts moving lift
  ↓
Frontend animates lift: 1 → 2 → 3 → 4 → 5
  ↓
When lift reaches floor 5:
  - Door opens
  - Request marked as served
  - Door closes
  ↓
Lift moves to next requested floor (SCAN order)
```

---

## 🔗 API ENDPOINTS

**Frontend Calls:**
```
GET /lifts
  ← Returns: {lifts: [{lift_id=1, current_floor, direction, door_status}]}

POST /requests?floor=5&lift_id=1
  ← Returns: {request_id, lift_id=1, status=pending}

GET /requests
  ← Returns: {requests: [{request_id, floor, lift_id=1, status}]}

GET /logs
  ← Returns: {logs: [{log_id, lift_id, event_type, event_time}]} (last 20)

GET /next_floor/1
  ← Returns: {next_floor, current_floor, direction} (SCAN result)

POST /simulate_lift_step/1
  ← Moves lift one step (called by background scheduler)
```

---

## 🎨 COMPONENT STRUCTURE

```
App.tsx
│
├── ControlPage (/)
│   ├── LiftVisualization
│   │   ├── Floor indicators (1-10)
│   │   ├── Animated lift box
│   │   └── Status display
│   │
│   ├── OutsidePanel
│   │   └── UP/DOWN buttons
│   │
│   ├── InsidePanel
│   │   └── Floor buttons (1-10)
│   │
│   └── RequestTable
│       └── Pending requests
│
└── DashboardPage (/dashboard)
    ├── LiftStatus
    ├── RequestQueue
    └── LogViewer (last 20)
```

---

## ✅ SUCCESS CRITERIA

When done, you should have:
- ✅ One lift (lift_id=1) working perfectly
- ✅ 10 floor buttons create requests
- ✅ Requests auto-assigned to lift_id=1
- ✅ Background scheduler moves lift automatically
- ✅ SCAN algorithm determines stop order
- ✅ Lift animates smoothly between floors
- ✅ Dashboard updates every 3 seconds
- ✅ All events logged and displayed
- ✅ Ready to scale to multiple lifts

---

## 🚀 FUTURE SCALING (AFTER PHASE 1)

When you add more lifts:
1. Insert into DB: `INSERT INTO lifts VALUES (2, 1, 'idle', 'closed')`
2. Modify `/requests` to accept `lift_id` parameter
3. Add SCAN logic to choose BEST lift (not just stop order)
4. Outside buttons (UP/DOWN) will call SCAN to pick best lift
5. Everything else stays the same!

---

**Now you have the CORRECT architecture for ONE lift!** 🚀

### Layer 3: FRONTEND (React)

**Two Main Pages:**

1. **Control Page (`/`)**
   - Visual: 10-floor building with animated lift shaft
   - Inside each floor: Buttons to call lift (Floor 1-10)
   - Request panel: Show which floor is selected
   - Display: Current lift position, direction, door status

2. **Dashboard Page (`/dashboard`)**
   - **Lifts Section**: Real-time status of all lifts (floor, direction, door)
   - **Requests Section**: 
     - Pending: Awaiting lift
     - Served: Already served
   - **Logs Section**: Event history (auto-updating)
   - **Polling**: Every 2 seconds fetches fresh data from backend

---

## 🔄 DATA FLOW (User's Perspective)

### Scenario 1: User on Floor 3 Calls Lift

```
1. USER ACTION (Frontend)
   User presses "Call Lift" button on Floor 3
   ↓
2. FRONTEND → BACKEND
   POST /requests?floor=3
   ↓
3. BACKEND Processing
   a) Save request to DB (status: "pending", floor: 3, lift_id: null)
   b) Run SCAN algorithm: Which lift should serve this?
      - Lift 1 is going UP at Floor 2 → Good candidate!
      - Lift 2 is going DOWN at Floor 8 → Not ideal
      → Assign Lift 1
   c) Update request: lift_id = 1, status = "pending"
   d) Create log: "Lift 1 assigned to Floor 3"
   ↓
4. BACKEND WORKS (Business Logic - NOT Frontend)
   - Lift 1 moves: Floor 2 → Floor 3 (animated by backend logic)
   - Create log: "Lift 1 arrived at Floor 3"
   - Lift 1 opens door, waits, closes door
   - Create log: "Door opened", "Door closed"
   - Lift continues to other floors per SCAN algorithm
   ↓
5. FRONTEND POLLING (Every 2 seconds)
   GET /lifts, GET /requests, GET /logs
   ↓
6. DASHBOARD UPDATES AUTOMATICALLY
   - Shows: "Lift 1 at Floor 3, Door Open"
   - Shows: Request #5 → "Served"
   - Shows: New logs of events
```

---

## 🎯 WHAT NEEDS TO BE BUILT

### Frontend Features

#### Control Page (/)
- **Left Side: Lift Visualization**
  - 10 floors displayed (F10, F9, F8...F1)
  - Animated lift box moving between floors
  - Show: Current floor, direction (↑↓), door status (open/closed)
  - Smooth animation as lift travels

- **Right Side: Floor Buttons + Controls**
  - Buttons for each floor (1-10)
  - When pressed → Show selected floor
  - Show feedback: "Floor 5 requested"
  - Auto-select a lift to animate

#### Dashboard Page (/dashboard)
- **Section 1: Lifts Status**
  - Grid of all lifts
  - Each shows: Lift ID, Current Floor, Direction, Door Status
  - Updates every 2 seconds via polling

- **Section 2: Request Queue**
  - Pending Requests: Awaiting service
  - Served Requests: Already completed
  - Each shows: Request ID, Floor, Assigned Lift, Time

- **Section 3: Event Logs**
  - Real-time list of all events
  - Timeline: Newest first
  - Events: "Lift 1 button pressed", "Door opened", "Arrived at Floor 5"

### Backend Features (Already Exists - Need to Verify)
- ✅ Lift endpoints (GET, PUT)
- ✅ Request endpoints (POST, GET, PUT)
- ✅ Log endpoints (GET, POST)
- ✅ SCAN algorithm in SchedulingService
- ✅ Auto-assign lifts when request created

---

## 🔌 POLLING MECHANISM

**Frontend Side:**
```
When DashboardPage loads:
1. Fetch initial data (lifts, requests, logs)
2. Set interval: Every 2 seconds
3. Call: GET /lifts, GET /requests, GET /logs
4. Update React state
5. Re-render UI with new data
6. Auto-scroll logs to show latest
```

**Why Polling?**
- Frontend ≠ Database (no direct connection)
- Frontend only talks to Backend API
- Backend queries DB and sends data
- Without polling: Frontend shows stale data until user refreshes

---

## 🧠 SCAN ALGORITHM EXPLAINED

### What it does:
Lifts move in one direction (UP/DOWN) until all requests in that direction are served, then reverse.

### Example:
```
Current: Lift at Floor 3, direction = UP
Pending requests: Floors 5, 7, 10 (going up), Floor 1 (going down)

SCAN Logic:
- While going UP: Visit 5, then 7, then 10
- Once at 10 with no more UP requests: Reverse to DOWN
- Now visit Floor 1 going DOWN
```

### Benefits:
- ✅ Minimizes total travel distance
- ✅ More efficient than random assignment
- ✅ Fair to all requests (no starvation)

---

## 📊 STATE MANAGEMENT

### What Data Lives Where?

**Backend (Database) - Source of Truth**
```
lifts: {lift_id, current_floor, direction, door_status}
requests: {request_id, floor, status, lift_id, request_time}
logs: {log_id, lift_id, event_type, event_time}
```

**Frontend (React State) - Temporary Copy**
```
ControlPage:
  - lifts: Lift[] (current state)
  - selectedLift: Lift (which lift to animate)
  - targetFloor: number (where user requested)
  - requests: Request[] (for serving manually)

DashboardPage:
  - lifts: Lift[]
  - requests: Request[]
  - logs: Log[]
```

---

## 🎬 IMPLEMENTATION STEPS (Your Journey)

### Phase 1: Setup (Already Done)
- ✅ React Router (2 pages: Control, Dashboard)
- ✅ API service (fetch functions)
- ✅ Basic component structure

### Phase 2: Control Page - Build Lift Visualization
1. Create floor buttons (10 floors)
2. Create lift animation canvas
3. Show selected floor input
4. Animate lift movement (1 floor/second)

### Phase 3: Request System
1. When user clicks floor → Create request via API
2. Backend auto-assigns lift
3. Update lift animation to requested floor

### Phase 4: Dashboard - Real-time Display
1. Setup polling (every 2 seconds)
2. Show all lifts status
3. Show all requests (pending + served)
4. Show all logs

### Phase 5: Connect Everything
1. Backend updates DB
2. Frontend polls and updates
3. Both pages stay in sync

---

## 📱 UI/UX FLOW

### User Opens App
```
↓
App loads on Control Page (/)
  ↓
Displays 10 floors with buttons
  ↓
Shows animated lift at Floor 1
  ↓
User clicks "Floor 5"
  ↓
Request sent to backend
  ↓
Backend assigns Lift (SCAN algorithm)
  ↓
Frontend animates lift: 1 → 2 → 3 → 4 → 5
  ↓
Frontend shows: "Lift arrived at Floor 5, Door Open"
  ↓
User can switch to Dashboard
  ↓
Dashboard shows real-time status
  - All lifts positions
  - All pending/served requests
  - All events happening
  ↓
Every 2 seconds: Dashboard refreshes with new data
```

---

## 🔗 API ENDPOINTS YOU'LL USE

**Frontend Calls:**
```
GET /lifts
  ← Returns: {lifts: [{lift_id, current_floor, direction, door_status}]}

POST /requests?floor=3
  ← Returns: {request_id, status: "pending"}

GET /requests
  ← Returns: {requests: [{request_id, floor, status, lift_id}]}

GET /logs
  ← Returns: {logs: [{log_id, lift_id, event_type, event_time}]}

PUT /requests/{request_id}
  ← Marks request as served

POST /assign_lift/{request_id}
  ← Manually trigger SCAN assignment (if auto-assign didn't happen)
```

---

## 🎨 COMPONENT STRUCTURE

```
App.tsx (with React Router)
│
├── Navigation Bar (Control | Dashboard)
│
├── ControlPage (/)
│   ├── LiftCanvas
│   │   ├── Floor markers (1-10)
│   │   ├── Animated lift box
│   │   ├── Door animation
│   │   └── Status display
│   │
│   └── RequestPanel
│       ├── Floor buttons (1-10)
│       ├── Request status
│       └── Manual serve controls (optional)
│
└── DashboardPage (/dashboard)
    ├── LiftsSection
    │   └── Grid of lift cards (status for each)
    │
    ├── RequestQueueSection
    │   ├── Pending requests table
    │   └── Served requests table
    │
    └── LogViewerSection
        └── Event log (auto-scrolling, latest first)
```

---

## 🚀 KEY CONCEPTS TO UNDERSTAND

### Concept 1: Request Lifecycle
```
PENDING → (Lift Assigned & Moving) → SERVED
```

### Concept 2: Lift Lifecycle
```
IDLE → (Request Received) → UP/DOWN → (Reached Floor) → DOOR_OPEN → DOOR_CLOSE → IDLE/NEXT_REQUEST
```

### Concept 3: Polling vs WebSocket
```
Polling (What we use):
Frontend asks backend every 2s: "Any updates?"
Backend: "Yes, Lift 1 moved to Floor 5"
Simple, works for small systems

WebSocket (Real-time):
Backend pushes: "Lift 1 just moved to Floor 5"
Faster, but more complex setup
```

### Concept 4: SCAN Algorithm
```
Don't pick random lift for each request.
Pick the lift that:
1. Is already moving in that direction
2. Is closest to that floor
3. Won't get overloaded
```

---

## 📝 WHAT YOU'LL CODE

### Files to Create/Modify
```
Frontend:
- src/pages/ControlPage.tsx - Floor buttons + lift animation
- src/pages/DashboardPage.tsx - Real-time dashboard
- src/components/LiftCanvas.tsx - Animated lift visualization
- src/components/FloorButtons.tsx - User interacts here
- src/App.css, src/App.pages.css - Styling

Backend (Already exists, might need tweaks):
- app/main.py - API endpoints (verify they exist)
- service/scheduling_service.py - SCAN algorithm
- repository/repository.py - Database queries
```

### Key Things to Handle
1. **Floor Selection UI** - User picks floor
2. **Animation Logic** - Lift moves smoothly
3. **Polling Loop** - Refresh every 2 seconds
4. **State Updates** - React state stays in sync
5. **Error Handling** - What if lift unavailable?
6. **UI Feedback** - Show user what's happening

---

## ✅ SUCCESS CRITERIA

When done, you should have:
- ✅ 10 floor buttons that create requests
- ✅ Lift animates when requested
- ✅ Dashboard shows real-time lift positions
- ✅ Dashboard shows pending/served requests
- ✅ Dashboard shows event logs
- ✅ SCAN algorithm assigns lifts automatically
- ✅ All pages sync via polling (2s interval)
- ✅ No manual "serve" button needed (auto-handled by backend)

---

## 🤔 COMMON MISCONCEPTIONS TO AVOID

❌ **DON'T**: Send lift movement commands from frontend
✅ **DO**: Frontend just requests, backend handles movement

❌ **DON'T**: Try to sync multiple lifts manually
✅ **DO**: Let SCAN algorithm decide which lift

❌ **DON'T**: Update DB directly from frontend
✅ **DO**: Call API endpoints, let backend update DB

❌ **DON'T**: Show stale data on dashboard
✅ **DO**: Poll every 2 seconds to stay current

---

## 🎓 LEARNING PATH

1. **Understand** this prompt completely
2. **Map** each requirement to a component
3. **Build** piece by piece (start small)
4. **Test** each piece before moving forward
5. **Integrate** pieces together
6. **Debug** using browser dev tools + backend logs

---

## 💡 TIPS FOR SUCCESS

1. **Start Simple**: Get 1 lift working first, then add more
2. **Debug Visually**: Use browser DevTools to see API calls
3. **Check Backend**: Verify SCAN algorithm is assigning lifts
4. **Test Polling**: Verify data updates every 2 seconds
5. **Log Everything**: Add console.logs to see data flow
6. **Mock Data**: If backend isn't ready, use fake data first

---

## 🆘 When You Get Stuck

Ask yourself:
- "Is this frontend or backend issue?"
- "Is data flowing from DB → API → Frontend?"
- "Is polling actually calling the API?"
- "Is React state updating?"
- "Are all endpoints working?"

Check backend logs:
```bash
# Terminal 1: Backend logs
tail -f backend/app/main.py output
```

Check frontend logs:
```bash
# Browser DevTools (F12):
console.log() to trace data
Network tab to see API calls
```

---

## 📚 REFERENCE: What Happens Behind Scenes

### When User Clicks "Floor 5" Button
```
FRONTEND                          BACKEND                    DATABASE
───────────────────────────────────────────────────────────────────

User clicks button
  ↓
POST /requests?floor=5
  ───────────────→ Receives request
                    ↓
                    Saves to DB: requests table
                    ↓
                    Run SCAN algorithm
                    - Check all lifts
                    - Find best one
                    - Assign Lift 1
                    ↓
                    Update DB: requests.lift_id = 1
                    ↓
                    Create log: "Assigned Lift 1"
                    ↓
                    Return: {request_id: 5, lift_id: 1}
                    ←─────────
Receives response
  ↓
Render: "Request created"
  ↓
Every 2 seconds:
GET /lifts ────→ Query DB: all lifts
                 Return current state
                 ←────
Update UI
  ↓
Show: "Lift 1 at Floor 5"
```

---

**Now you understand the full system!** 

Start building piece by piece. Good luck! 🚀
