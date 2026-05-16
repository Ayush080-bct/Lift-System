from fastapi import FastAPI
from backend.model.models import Lift, Request, Log
from backend.repository.repository import LiftRepository

app=FastAPI()
repo=LiftRepository()
@app.get("/")
def root():
    return {"Message":"Lift System API running"}
@app.get('/lifts/{lift_id}')
def lift_status(lift_id:int):
    result=repo.get_lift(lift_id)
    if result:
        return {'lift_id':result[0],'floor':result[1]}
    return {'error':"lift not found"}
@app.get('/lifts')
def lifts_status():
    result=repo.get_all_lifts()
    if result:
        return {"lifts": [{"lift_id": lift.lift_id, "current_floor": lift.current_floor, "direction": lift.direction, "door_status": lift.door_status} for lift in result]}
    return {'error':"lifts status not found"}
@app.put('/lifts/{lift_id}')
def move_lift(lift_id:int,floor:int,direction:str,door_status:str):
    result=repo.move_lift(lift_id,floor,direction,door_status)
    if result:
        return {'Message':'Lift_moved Sucessfully','lift_id':lift_id,'floor':floor,'direction':direction,'door_status':door_status}
    return {'Error':'Falied to move the lift'}
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