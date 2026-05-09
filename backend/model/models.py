from dataclasses import dataclass
from datetime import datetime
@dataclass
class Lift:
    lift_id:int
    current_floor:int
    direction : str
    door_status: str
@dataclass
class Request:
    request_id:int
    floor:int
    request_time:datetime
    status:str
    lift_id:int


@dataclass
class Log:
    log_id: int
    lift_id: int
    event_type: str
    event_time: datetime
