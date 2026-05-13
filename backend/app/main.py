from fastapi import FastAPI
from model.models import  Lift,Request,Log
from repository.repository import LiftRepository
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


