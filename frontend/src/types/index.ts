//an interface is a way to define the shape of an object — 
// basically a contract that says: “Any object of this type must have these properties, with these types.”
//It doesn’t generate code at runtime; it’s purely for type checking during development.
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