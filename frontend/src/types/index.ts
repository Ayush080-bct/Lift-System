export interface Lift{
    lift_id:number;
    current_floor:number;
    direction:"up"|"down"|"idle";
    door_status:"open"|"closed";
}
export interface Request{
    request_id:number;
    floor:number;
    request_time:string;
    status:"pending"|"served";
    lift_id:Number|null;
}
export interface Log{
    log_id:number;
    lift_id:Number|null;
    event_type:"button_pressed"|"lift_arrived"|"door_opened"|"door_closed"|"emergency_stop";
    event_time:string;
}