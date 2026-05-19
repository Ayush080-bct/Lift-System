# Lift System Backend

A simple backend project that simulates the working of a lift (elevator) system.  
This project demonstrates how to design structured databases, implement scheduling algorithms, and expose REST APIs for managing lift requests, states, and logs.

## 🚀 Features
- Track lift state (current floor, direction, door status)
- Handle floor requests (internal and external calls)
- Scheduling algorithm to assign lifts efficiently
- Log events for safety and maintenance
- Built with PostgreSQL for structured data and reliability

## To run server
- fastapi dev backend/app/main.py

## 📡 API Endpoints

### GET Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /` | Health check - returns API status |
| `GET /lifts/{lift_id}` | Get specific lift status by ID (returns lift_id and current_floor) |
| `GET /lifts` | Get all lifts status with full details (lift_id, current_floor, direction, door_status) |
| `GET /requests` | Get all pending requests |
| `GET /logs` | Get all event logs |

### PUT Endpoints
| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `PUT /lifts/{lift_id}` | Update lift position and status | `lift_id` (path), `floor`, `direction`, `door_status` (query) |
| `PUT /requests/{request_id}` | Mark request as served | `request_id` (path parameter) |

### POST Endpoints
| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `POST /requests` | Create a new lift request | `floor` (query parameter) |
| `POST /logs` | Add a new event log | `lift_id`, `event_type` (query parameters) |

## 🏗️ Architecture

### Repository Pattern (Data Access Layer)
The project uses the **Repository Pattern** to separate database operations from business logic:

**Benefits:**
- ✅ Clean separation between data access and business logic
- ✅ Easy to test (can mock repository)
- ✅ Reusable across multiple services
- ✅ Centralized database queries

**Layers:**
1. **Model Layer** (`backend/model/`) - Data structures
2. **Repository Layer** (`backend/repository/`) - Database operations
3. **Service Layer** (`backend/service/`) - Business logic (SCAN algorithm)
4. **API Layer** (`backend/app/`) - FastAPI endpoints

## 🤖 SCAN Algorithm (Scheduling Service)

The lift system uses the **SCAN Algorithm** (elevator algorithm) for efficient scheduling:

### How it works:
1. **Lift moves in one direction** until all requests in that direction are served
2. **Reverses direction** when no more requests ahead
3. **Picks closest lift** that's already moving toward the requested floor
4. **Load balancing** - avoids assigning >5 requests to one lift

### Example:
```
Lift 1: floor 3, moving UP
Request: floor 7

Action: Assign Lift 1 (already moving up, closer to floor 7)
Scoring: distance=4, load=2 requests → score = 4 + (2*2) = 8
```

## 📊 Data Models

### Lift
```python
@dataclass
class Lift:
    lift_id: int           # Unique identifier
    current_floor: int     # Current position (0-10)
    direction: str         # "up", "down", or "idle"
    door_status: str       # "open" or "closed"
```

### Request
```python
@dataclass
class Request:
    request_id: int        # Unique identifier
    floor: int             # Requested floor
    request_time: datetime # When request was made
    status: str            # "pending" or "served"
    lift_id: int           # Assigned lift (nullable)
```

### Log
```python
@dataclass
class Log:
    log_id: int            # Unique identifier
    lift_id: int           # Which lift
    event_type: str        # Event description
    event_time: datetime   # When event occurred
```

## 🔗 Additional Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `PUT /requests/{request_id}` | PUT | Mark request as served |
| `POST /logs` | POST | Log an event |
| `GET /logs` | GET | Get all event logs |

## 🚨 Error Handling

The API includes comprehensive error handling:
- **400**: Bad request (negative floors, invalid direction)
- **404**: Resource not found (lift/request doesn't exist)
- **500**: Server error (unexpected exceptions)

## 🗄️ Database

### Tables
- **lifts** - Lift status and position
- **requests** - Floor requests with status
- **logs** - Event records for auditing

Run schema setup:
```bash
psql -U your_user -d lift_system -f backend/database/Schema.sql
```
    cursor.close()
    return {"lift_id": result[0], "floor": result[1]}
```
❌ Database code scattered everywhere
❌ Hard to test without a real database
❌ Duplicate queries in multiple endpoints
❌ Difficult to switch databases (PostgreSQL → MongoDB)

**With Repository (Best Practice):**
```python
# repository/repository.py (Data Access)
class LiftRepository:
    def get_lift(self, lift_id: int):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lifts WHERE lift_id = %s", (lift_id,))
        return cursor.fetchone()

# app/main.py (Business Logic)
@app.get("/lift_status/{lift_id}")
def lift_status(lift_id: int):
    result = repo.get_lift(lift_id)
    return {"lift_id": result[0], "floor": result[1]}
```
✅ All database logic in ONE place
✅ Easy to mock for testing
✅ No code duplication
✅ Easy to switch databases later
✅ Clean separation: Model → Repository → Controller