from fastapi import FastAPI,HTTPException
from backend.model.models import Lift, Request, Log
from backend.repository.repository import LiftRepository
from backend.service.scheduling_service import SchedulingService
from contextlib import asynccontextmanager
import asyncio

from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app=FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo=LiftRepository()
scheduler=SchedulingService(repo)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Unexpected server error", "details": str(exc)}
    )
@app.get("/")
def root():
    return {"message":"Lift System API running"}
@app.get('/lifts/{lift_id}')
def lift_status(lift_id:int):
    try:
        result=repo.get_lift(lift_id)
        if result:
            return {'lift_id':result[0],'floor':result[1]}
        raise HTTPException(status_code=404, detail="Lift not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get('/lifts')
def lifts_status():
    try:
        result=repo.get_all_lifts()
        if result:
            return {"lifts": [{"lift_id": lift.lift_id, "current_floor": lift.current_floor, "direction": lift.direction, "door_status": lift.door_status} for lift in result]}
        return {"lifts": []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.put("/lifts/{lift_id}")
def move_lift(lift_id: int, floor: int, direction: str, door_status: str):
    try:
        if floor < 0:
            raise HTTPException(status_code=400, detail="Floor cannot be negative")
        if direction not in ["up", "down", "idle"]:
            raise HTTPException(status_code=400, detail="Direction must be 'up', 'down', or 'idle'")
        if door_status not in ["open", "closed"]:
            raise HTTPException(status_code=400, detail="Door status must be 'open' or 'closed'")
        result = repo.move_lift(lift_id, floor, direction, door_status)
        if result:
            return {
                "message": "Lift moved successfully",
                "lift_id": lift_id,
                "floor": floor,
                "direction": direction,
                "door_status": door_status
            }
        raise HTTPException(status_code=404, detail="Lift not found")
    except psycopg2.errors.CheckViolation as e:
        raise HTTPException(status_code=400, detail="Invalid input: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post('/requests')
def position_request(floor:int,lift_id:int=1):#floor is the query parameter in endpoint
    try:
        if floor < 0:
            raise HTTPException(status_code=400, detail="Floor cannot be negative")
        result=repo.add_request(floor)
        if result:
            # Assign request to lift immediately
            repo.assign_request_to_lift(result, lift_id)
            repo.log_event(lift_id, f"Request {result} created for floor {floor}")
            return {'message':'Request added successfully','request_id':result,'floor':floor,'lift_id':lift_id,'status':'pending'}
        raise HTTPException(status_code=500, detail="Failed to add request")
    except psycopg2.errors.CheckViolation as e:
        raise HTTPException(status_code=400, detail="Invalid input: " + str(e))
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail="Lift not found: " + str(e))
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=409, detail="Duplicate request: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/requests')
def get_all_position_request():
    try:
        result=repo.get_pending_request()
        if result:
            return {'requests':[{'request_id':request.request_id,
                                'floor':request.floor,
                                'request_time':request.request_time,
                                'status':request.status,
                                'lift_id':request.lift_id
                }for request in result]}
        return {"requests": []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
@app.put('/requests/{request_id}')
def change_status(request_id:int):
    try:
        # Get request details BEFORE deleting
        pending_requests = repo.get_pending_request()
        request_obj = next((r for r in pending_requests if r.request_id == request_id), None)
        
        if not request_obj:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Delete the request
        result = repo.mark_served(request_id)
        
        if result:
            # Create log entry
            repo.log_event(request_obj.lift_id, f"Served request {request_id} for floor {request_obj.floor}")
            return {'message':'Pending request served successfully','request_id':request_id}
        
        raise HTTPException(status_code=404, detail="Failed to serve request")
    except psycopg2.errors.CheckViolation as e:
        raise HTTPException(status_code=400, detail="Invalid input: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/logs")
def add_log(lift_id: int, event_type: str):
    try:
        if not event_type or len(event_type) == 0:
            raise HTTPException(status_code=400, detail="Event type cannot be empty")
        result = repo.log_event(lift_id, event_type)
        if result:
            return {
                "message": "Log added successfully",
                "lift_id": lift_id,
                "event_type": event_type
            }
        raise HTTPException(status_code=500, detail="Failed to add log")
    except psycopg2.errors.CheckViolation as e:
        raise HTTPException(status_code=400, detail="Invalid input: " + str(e))
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail="Lift not found: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/logs")
def get_all_logs():
    try:
        result = repo.get_all_logs()
        if result:
            return {
                "logs": [
                    {
                        "log_id": log.log_id,
                        "lift_id": log.lift_id,
                        "event_type": log.event_type,
                        "event_time": log.event_time
                    }
                    for log in result
                ]
            }
        return {"logs": []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@app.get("/next_floor/{lift_id}")
def get_next_floor(lift_id: int):
    """
    Get the next floor a lift should visit based on pending requests (SCAN algorithm).
    """
    try:
        lift = repo.get_lift(lift_id)
        
        if not lift:
            raise HTTPException(status_code=404, detail="Lift not found")
        
        next_floor = scheduler.get_next_floor_for_lift(lift_id)
        
        if next_floor is None:
            return {
                "message": "No pending requests",
                "lift_id": lift_id,
                "next_floor": None,
                "current_floor": lift.current_floor
            }
        
        return {
            "message": "Next floor determined",
            "lift_id": lift_id,
            "current_floor": lift.current_floor,
            "next_floor": next_floor,
            "direction": lift.direction
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulate_lift_step/{lift_id}")
def simulate_lift_step(lift_id: int):
    """
    Simulate one step of lift movement: move floor, serve requests, and log events.
    This is the engine that makes lifts move automatically following SCAN algorithm.
    """
    try:
        lift = repo.get_lift(lift_id)
        
        if not lift:
            raise HTTPException(status_code=404, detail="Lift not found")
        
        # Execute one simulation step
        scheduler.update_and_serve(lift_id)
        
        # Get updated lift status
        updated_lift = repo.get_lift(lift_id)
        
        return {
            "message": "Lift step executed",
            "lift_id": lift_id,
            "current_floor": updated_lift.current_floor,
            "direction": updated_lift.direction,
            "door_status": updated_lift.door_status
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def simulate_lifts():
    """Background task to continuously move lifts"""
    while True:
        try:
            # For each lift, simulate one step
            lifts = repo.get_all_lifts()
            for lift in lifts:
                scheduler.update_and_serve(lift.lift_id)
            await asyncio.sleep(2)  # Every 2 seconds
        except Exception as e:
            print(f"Error in lift simulation: {e}")
            await asyncio.sleep(2)

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: start background task
    task = asyncio.create_task(simulate_lifts())
    yield
    # Shutdown: cancel task
    task.cancel()
