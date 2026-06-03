import type { Lift, Request, Log } from "../types";

const API_URL = "http://localhost:8000";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
    const msg =
      typeof errorData.detail === "string"
        ? errorData.detail
        : errorData.error || `HTTP ${response.status}`;
    throw new Error(msg);
  }
  return response.json();
}

export async function getAllLifts(): Promise<Lift[]> {
  const data = await handleResponse<{ lifts: Lift[] }>(
    await fetch(`${API_URL}/lifts`)
  );
  return data.lifts ?? [];
}

export async function getLift(lift_id: number): Promise<Lift> {
  return handleResponse<Lift>(await fetch(`${API_URL}/lifts/${lift_id}`));
}

export async function createRequest(floor: number) {
  const params = new URLSearchParams({ floor: String(floor) });
  return handleResponse<{
    request_id: number;
    floor: number;
    lift_id: number;
    status: string;
    message: string;
  }>(await fetch(`${API_URL}/requests?${params}`, { method: "POST" }));
}

export async function getRequests(): Promise<Request[]> {
  const data = await handleResponse<{ requests: Request[] }>(
    await fetch(`${API_URL}/requests`)
  );
  return data.requests ?? [];
}

export async function getLogs(): Promise<Log[]> {
  const data = await handleResponse<{ logs: Log[] }>(
    await fetch(`${API_URL}/logs`)
  );
  return data.logs ?? [];
}

export async function getNextFloor(lift_id: number): Promise<{
  lift_id: number;
  current_floor: number;
  next_floor: number | null;
  direction: Lift["direction"];
  queue: number[];
}> {
  return handleResponse(await fetch(`${API_URL}/next_floor/${lift_id}`));
}
