from fastapi import FastAPI,HTTPException
from backend.model.models import Lift, Request, Log
from backend.repository.repository import LiftRepository
import psycopg2#
app=FastAPI()
repo=LiftRepository()
@app.get("/")
def root():
    return {"Message":"Lift System API running"}
@app.get('/lifts/{lift_id}')
def lift_status(lift_id:int):
    try:
        result=repo.get_lift(lift_id)
        if result:
            return {'lift_id':result[0],'floor':result[1]}
        raise HTTPException(status_code=404, detail="Lift not found")#request resources not found
    except Exception as e:
        #raise a 500 for unexpected error
        raise HTTPException(status_code=500, detail=str(e))# Internal server error
@app.get('/lifts')
def lifts_status():
    try:
        result=repo.get_all_lifts()
        if result:
            return {"lifts": [{"lift_id": lift.lift_id, "current_floor": lift.current_floor, "direction": lift.direction, "door_status": lift.door_status} for lift in result]}
        raise HTTPException(status_code=404, detail="Lifts not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.put("/lifts/{lift_id}")
def move_lift(lift_id: int, floor: int, direction: str, door_status: str):
    try:
        result = repo.move_lift(lift_id, floor, direction, door_status)
        if result:
            return {
                "Message": "Lift moved successfully",
                "lift_id": lift_id,
                "floor": floor,
                "direction": direction,
                "door_status": door_status
            }
        raise HTTPException(status_code=404, detail="Lift not found")#If the lift does not exist
    except psycopg2.errors.CheckViolation as e:#since our database have check constraints , the invalid input will rejected by database
        # Database rejected invalid direction/door_status
        raise HTTPException(status_code=400, detail="Invalid input: " + str(e))#Bad input (eg invalid direction or door_status)
    except Exception as e:
        # Unexpected server error
        raise HTTPException(status_code=500, detail=str(e))
@app.post('/requests')
def postion_request(floor:int):
    result=repo.add_request(floor)
    if result:
        return {'Message':'Request added sucessfully','request_id':result,'floor':floor,'status':'pending'}
    return {'Error':'Failed to add request'}
@app.get('/requests')
def get_all_position_request():
    result=repo.get_pending_request()
    if result:
        return {'Request':[{'request_id':request.request_id,
                            'floor':request.floor,
                            'request_time':request.request_time,
                            'status':request.status,
                            'lift_id':request.lift_id
            }for request in result]}
    return {"Error":"falied to get all pending request"}
@app.put('/requests/{request_id}')
def change_status(request_id:int):
    result=repo.mark_served(request_id)
    if result:
        return {'Message':'Pending request served sucessfullly','request_id':request_id}
    return {'Error':'Failed to serve'}
@app.post('/logs')
def add_log(lift_id:int,event_type:str):
    result=repo.log_event(lift_id,event_type)
    if result:
        return {'Message':'Log Added in Database','lift_id':lift_id,'event_type':event_type}
    return {'Error':'Failed to add log'}
@app.get('/logs')
def get_all_logs():
    result=repo.get_all_logs()
    if result:
        return {'logs': [{'log_id': log.log_id, 'lift_id': log.lift_id, 'event_type': log.event_type, 'event_time': log.event_time} for log in result]}
    return {'error': 'No logs found'}