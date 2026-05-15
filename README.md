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
| `GET /lift_Status/{lift_id}` | Get specific lift status by ID (returns lift_id and current_floor) |
| `GET /lifts_Status` | Get all lifts status with full details (lift_id, current_floor, direction, door_status) |

### PUT Endpoints
| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `PUT /move_lift/{lift_id}` | Update lift position and status | `lift_id` (path), `floor`, `direction`, `door_status` (query) |

### POST Endpoints
| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `POST /position_request/{floor}` | Create a new lift request | `floor` (path parameter) |

## Architecture

### Repository Pattern (Data Access Layer)
The project uses the **Repository Pattern** to separate database operations from business logic:

**Without Repository (Bad Practice):**
```python
@app.get("/lift_status/{lift_id}")
def lift_status(lift_id: int):
    cursor = conn.cursor()  # DB code mixed with API logic
    cursor.execute("SELECT * FROM lifts WHERE lift_id = %s", (lift_id,))
    result = cursor.fetchone()
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