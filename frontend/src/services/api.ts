import type { Lift, Request, Log } from "../types";

const API_URL = "http://localhost:8000";

// ✅ ADDED: Centralized error handler — checks HTTP status before parsing JSON
async function handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
}

export async function getAllLifts(): Promise<Lift[]> { // typescript return type notation similar to python(->)
    const response = await fetch(`${API_URL}/lifts`);
    const data = await handleResponse<{ lifts: Lift[] }>(response);
    return data.lifts || [];
}

export async function createRequest(floor: number, lift_id: number = 1) {
    const params = new URLSearchParams({ floor: String(floor), lift_id: String(lift_id) }); // ✅ ADDED: Safe URL encoding
    const response = await fetch(`${API_URL}/requests?${params.toString()}`, {
        method: "POST",
    });
    return handleResponse(response); // ✅ FIXED: Validate response before returning
}

export async function getRequests(): Promise<Request[]> {
    const response = await fetch(`${API_URL}/requests`); // raw json from server
    const data = await handleResponse<{ requests: Request[] }>(response); // ✅ FIXED: Validate + type-safe parse
    return data.requests || []; // convert response body(text/bit stream) to js object
}

export async function getLogs(): Promise<Log[]> {
    const response = await fetch(`${API_URL}/logs`);
    const data = await handleResponse<{ logs: Log[] }>(response); // ✅ FIXED: Validate + type-safe parse
    return data.logs || [];
}

export async function getAlift(lift_id: number): Promise<Lift> {
    const response = await fetch(`${API_URL}/lifts/${lift_id}`);
    const data = await handleResponse<{ lift_id: number; current_floor: number; direction: string; door_status: string }>(response); // ✅ FIXED: Validate response
    // ✅ FIXED: Map raw API response to proper Lift type
    return {
        lift_id: data.lift_id,
        current_floor: data.current_floor,
        direction: data.direction,
        door_status: data.door_status
    };
}

export async function updateLift(
    lift_id: number,
    floor: number,
    direction: string,
    door_status: string
) {
    const params = new URLSearchParams({ floor: String(floor), direction, door_status }); // ✅ ADDED: Safe URL encoding
    const response = await fetch(
        `${API_URL}/lifts/${lift_id}?${params.toString()}`, // ✅ FIXED: URL-encoded params
        { method: "PUT" }
    );
    return handleResponse(response); // ✅ FIXED: Validate response before returning
}

export async function serveRequest(request_id: number) {
    const response = await fetch(`${API_URL}/requests/${request_id}`,
        {
            method: "PUT"
        }
    );
    return handleResponse(response); // ✅ FIXED: Validate response before returning
}

export async function getNextFloor(lift_id: number) {
    const response = await fetch(`${API_URL}/next_floor/${lift_id}`);
    return handleResponse(response); // ✅ FIXED: Validate response before returning
}

export async function simulateLiftStep(lift_id: number) {
    const response = await fetch(`${API_URL}/simulate_lift_step/${lift_id}`,
        {
            method: "POST"
        }
    );
    return handleResponse(response); // ✅ FIXED: Validate response before returning
}