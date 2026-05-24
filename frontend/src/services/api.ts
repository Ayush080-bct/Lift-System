import type { Lift,Request,Log } from "../types";

const API_URL="http://localhost:8000";
export async function getAllLifts():Promise<Lift[]> {//typescript return type notation similar to python(->)
    const response=await fetch(`${API_URL}/lifts`);
    const data=await response.json();
    return data.lifts || [];
}
export async function createRequest(floor:number){
    const response=await fetch(`${API_URL}/requests?floor=${floor}`,{
        method:"POST",
    });
    return response.json();
}
export async function getRequests():Promise<Request[]>{
    const response=await fetch(`${API_URL}/requests`);//raw json from server
    const data=await response.json();//convert response body(text/bit stream) to js object
    return data.requests || [];
}
export async function getLogs():Promise<Log[]>{
    const response=await fetch(`${API_URL}/logs`);
    const data=await response.json()
    return data.logs || [];    
}
export async function getAlift(lift_id:number):Promise<Lift>{
    const response=await fetch(`${API_URL}/lifts/${lift_id}`)
    const data=await response.json();
    return data;
}
export async function updateLift(
    lift_id:number,
    floor:number,
    direction:string,
    door_status:string
) {
    const response=await fetch(
        `${API_URL}/lifts/${lift_id}?floor=${floor}&direction=${direction}&door_status=${door_status}`,
        { method : "PUT" }
    );
    return response.json();
}
export async function serveRequest(request_id:number) {
    const response=await fetch(`${API_URL}/requests/${request_id}`,
        {
            method:"PUT"
        }
    );   
    return response.json();
}

export async function assignLift(request_id:number) {
    const response=await fetch(`${API_URL}/assign_lift/${request_id}`,
        {
            method:"POST"
        });
        if(!response.ok){
            throw new Error("Failed to assign lift");
        }

    return response.json();
}
export async function getNextFloor(lift_id: number) {
    const response = await fetch(`${API_URL}/next_floor/${lift_id}`);
    return response.json();
}
