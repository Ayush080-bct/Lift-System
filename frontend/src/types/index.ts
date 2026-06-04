export interface Lift {
  lift_id: number;
  current_floor: number;
  direction: "up" | "down" | "idle";
  door_status: "open" | "closed";
}

export interface Request {
  request_id: number;
  floor: number;
  request_time: string;
  status: "pending" | "served";
  lift_id: number | null;
}

export type LogEventType =
  | "button_pressed"
  | "lift_arrived"
  | "door_opened"
  | "door_closed"
  | "emergency_stop";

export interface Log {
  log_id: number;
  lift_id: number;
  event_type: LogEventType;
  event_time: string;
}
