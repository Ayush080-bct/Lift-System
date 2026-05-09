from fastapi import FastAPI
from model.models import  Lift,Request,Log
app=FastAPI()

@app.get("/")
def root():
    return {"Message":"Lift System API running"}


