from fastapi import FastAPI,HTTPException
from backend.model.models import Lift, Request, Log
from backend.repository.repository import LiftRepository
from backend.service.scheduling_service import SchedulingService

from fastapi.responses import JSONResponse
from fastapi.requests import Request
import psycopg2
app=FastAPI()
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
def position_request(floor:int):#floor is the queer parameter in endpoint
    try:
        if floor < 0:
            raise HTTPException(status_code=400, detail="Floor cannot be negative")
        result=repo.add_request(floor)
        if result:
            return {'message':'Request added successfully','request_id':result,'floor':floor,'status':'pending'}
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
        result=repo.mark_served(request_id)
        if result:
            return {'message':'Pending request served successfully','request_id':request_id}
        raise HTTPException(status_code=404, detail="Request not found")
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


@app.post("/assign_lift/{request_id}")
def assign_lift_auto(request_id: int):
    """
    Automatically assign the best lift to a request using SCAN algorithm.
    """
    try:
        # Get the request details
        result = repo.get_pending_request()
        request_obj = next((r for r in result if r.request_id == request_id), None)
        
        if not request_obj:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Find best lift for this floor
        best_lift_id = scheduler.assign_lift_to_request(request_obj.floor)
        
        if not best_lift_id:
            raise HTTPException(status_code=500, detail="No lifts available")
        
        # Assign request to lift
        success = repo.assign_request_to_lift(request_id, best_lift_id)
        
        if success:
            repo.log_event(best_lift_id, f"Assigned to request {request_id} for floor {request_obj.floor}")
            return {
                "message": "Lift assigned successfully",
                "request_id": request_id,
                "lift_id": best_lift_id,
                "floor": request_obj.floor
            }
        
        raise HTTPException(status_code=500, detail="Failed to assign lift")
    
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