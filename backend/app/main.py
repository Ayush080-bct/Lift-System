import asyncio
from contextlib import asynccontextmanager

import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from repository.repository import LiftRepository
from service.scheduling_service import SchedulingService

repo = LiftRepository()
scheduler = SchedulingService(repo)

MIN_FLOOR = 1
MAX_FLOOR = 10


def _lift_json(lift):
    return {
        "lift_id": lift.lift_id,
        "current_floor": lift.current_floor,
        "direction": lift.direction,
        "door_status": lift.door_status,
    }


async def simulate_lifts():
    while True:
        try:
            lifts = await run_in_threadpool(repo.get_all_lifts)
            for lift in lifts:
                await run_in_threadpool(scheduler.update_and_serve, lift.lift_id)
        except Exception as e:
            print(f"Error in lift simulation: {e}")
        await asyncio.sleep(2)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(simulate_lifts())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return JSONResponse(
        status_code=500,
        content={"error": "Unexpected server error", "details": str(exc)},
    )


@app.get("/")
async def root():
    return {"message": "Lift System API running"}


@app.get("/lifts/{lift_id}")
async def lift_status(lift_id: int):
    lift = await run_in_threadpool(repo.get_lift, lift_id)
    if not lift:
        raise HTTPException(status_code=404, detail="Lift not found")
    return _lift_json(lift)


@app.get("/lifts")
async def lifts_status():
    lifts = await run_in_threadpool(repo.get_all_lifts)
    return {"lifts": [_lift_json(lift) for lift in lifts]}


@app.put("/lifts/{lift_id}")
async def move_lift(lift_id: int, floor: int, direction: str, door_status: str):
    if floor < MIN_FLOOR or floor > MAX_FLOOR:
        raise HTTPException(status_code=400, detail=f"Floor must be between {MIN_FLOOR} and {MAX_FLOOR}")
    if direction not in ("up", "down", "idle"):
        raise HTTPException(status_code=400, detail="Invalid direction")
    if door_status not in ("open", "closed"):
        raise HTTPException(status_code=400, detail="Invalid door status")

    ok = await run_in_threadpool(repo.move_lift, lift_id, floor, direction, door_status)
    if not ok:
        raise HTTPException(status_code=404, detail="Lift not found")
    return {"message": "Lift updated", **_lift_json(await run_in_threadpool(repo.get_lift, lift_id))}


@app.post("/requests")
async def create_request(floor: int):
    if floor < MIN_FLOOR or floor > MAX_FLOOR:
        raise HTTPException(status_code=400, detail=f"Floor must be between {MIN_FLOOR} and {MAX_FLOOR}")

    try:
        request_id = await run_in_threadpool(repo.add_request, floor)
        if not request_id:
            raise HTTPException(status_code=500, detail="Failed to add request")

        lift_id = await run_in_threadpool(scheduler.assign_lift_to_request, floor)
        if not lift_id:
            raise HTTPException(status_code=503, detail="No lifts available")

        await run_in_threadpool(repo.assign_request_to_lift, request_id, lift_id)
        await run_in_threadpool(repo.log_event, lift_id, "button_pressed")

        return {
            "message": "Request added successfully",
            "request_id": request_id,
            "floor": floor,
            "lift_id": lift_id,
            "status": "pending",
        }
    except psycopg2.errors.CheckViolation as e:
        raise HTTPException(status_code=400, detail=str(e))
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/requests")
async def get_requests():
    pending = await run_in_threadpool(repo.get_pending_request)
    return {
        "requests": [
            {
                "request_id": r.request_id,
                "floor": r.floor,
                "request_time": r.request_time,
                "status": r.status,
                "lift_id": r.lift_id,
            }
            for r in pending
        ]
    }


@app.put("/requests/{request_id}")
async def serve_request(request_id: int):
    pending = await run_in_threadpool(repo.get_pending_request)
    req = next((r for r in pending if r.request_id == request_id), None)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    ok = await run_in_threadpool(repo.mark_served, request_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Failed to serve request")

    if req.lift_id:
        await run_in_threadpool(repo.log_event, req.lift_id, "lift_arrived")

    return {"message": "Request served", "request_id": request_id}


@app.post("/logs")
async def add_log(lift_id: int, event_type: str):
    allowed = {"button_pressed", "lift_arrived", "door_opened", "door_closed", "emergency_stop"}
    if event_type not in allowed:
        raise HTTPException(status_code=400, detail=f"event_type must be one of {allowed}")

    log_id = await run_in_threadpool(repo.log_event, lift_id, event_type)
    if not log_id:
        raise HTTPException(status_code=500, detail="Failed to add log")
    return {"message": "Log added", "log_id": log_id, "lift_id": lift_id, "event_type": event_type}


@app.get("/logs")
async def get_logs():
    logs = await run_in_threadpool(repo.get_all_logs)
    return {
        "logs": [
            {
                "log_id": log.log_id,
                "lift_id": log.lift_id,
                "event_type": log.event_type,
                "event_time": log.event_time,
            }
            for log in logs
        ]
    }


@app.get("/next_floor/{lift_id}")
async def get_next_floor(lift_id: int):
    lift = await run_in_threadpool(repo.get_lift, lift_id)
    if not lift:
        raise HTTPException(status_code=404, detail="Lift not found")

    next_floor = await run_in_threadpool(scheduler.get_next_floor_for_lift, lift_id)
    queue = await run_in_threadpool(scheduler.get_scan_queue, lift_id)

    return {
        "lift_id": lift_id,
        "current_floor": lift.current_floor,
        "next_floor": next_floor,
        "direction": lift.direction,
        "queue": queue,
    }


@app.post("/simulate_lift_step/{lift_id}")
async def simulate_lift_step(lift_id: int):
    lift = await run_in_threadpool(repo.get_lift, lift_id)
    if not lift:
        raise HTTPException(status_code=404, detail="Lift not found")

    await run_in_threadpool(scheduler.update_and_serve, lift_id)
    updated = await run_in_threadpool(repo.get_lift, lift_id)
    return {"message": "Lift step executed", **_lift_json(updated)}
