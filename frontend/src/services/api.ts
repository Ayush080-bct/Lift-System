import type { Lift } from "../types";
const API_URL="http://localhost:8000";
export async function getAllLifts():Promise<Lift[]> {
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