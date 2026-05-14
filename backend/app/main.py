from fastapi import FastAPI
from backend.model.models import Lift, Request, Log
from backend.repository.repository import LiftRepository

app=FastAPI()
repo=LiftRepository()
@app.get("/")
def root():
    return {"Message":"Lift System API running"}
@app.get('/lift_Status/{lift_id}')
def lift_status(lift_id:int):
    result=repo.get_lift(lift_id)
    if result:
        return {'lift_id':result[0],'floor':result[1]}
    return {'error':"lift not found"}
@app.get('/lifts_Status')
def lifts_status():
    result=repo.get_all_lifts()
    if result:
        return {"lifts": [{"lift_id": lift.lift_id, "current_floor": lift.current_floor, "direction": lift.direction, "door_status": lift.door_status} for lift in result]}
    return {'error':"lifts status not found"}
@app.put('move_lift/{lift_id}')
def move_lift(lift_id:int,floor:int,direction:str,door_status:str):
    result=repo.move_lift(lift_id,floor,direction,door_status)
    if result:
        return {'Message':'Lift_moved Sucessfully','lift_id':lift_id,'floor':floor,'direction':direction,'door_status':door_status}
    return {'Error':'Falied to move the lift'}