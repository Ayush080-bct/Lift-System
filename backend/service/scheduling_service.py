"""
SCAN scheduling: one direction until no more stops ahead, then reverse.
"""

from backend.repository.repository import LiftRepository

MAX_LOAD = 5


class SchedulingService:
    def __init__(self, repo: LiftRepository):
        self.repo = repo

    def assign_lift_to_request(self, requested_floor: int) -> int | None:
        lifts = self.repo.get_all_lifts()
        if not lifts:
            return None

        pending = self.repo.get_pending_request()
        load = {lift.lift_id: 0 for lift in lifts}
        for req in pending:
            if req.lift_id:
                load[req.lift_id] += 1

        best_lift = None
        best_score = float("inf")

        for lift in lifts:
            if load[lift.lift_id] > MAX_LOAD:
                continue

            if lift.direction == "up" and lift.current_floor < requested_floor:
                distance = requested_floor - lift.current_floor
            elif lift.direction == "down" and lift.current_floor > requested_floor:
                distance = lift.current_floor - requested_floor
            elif lift.direction == "idle":
                distance = abs(lift.current_floor - requested_floor)
            else:
                distance = abs(lift.current_floor - requested_floor) + 10

            score = distance + load[lift.lift_id] * 2
            if score < best_score:
                best_score = score
                best_lift = lift

        if best_lift is None:
            best_lift = min(lifts, key=lambda l: abs(l.current_floor - requested_floor))

        return best_lift.lift_id

    def get_scan_queue(self, lift_id: int) -> list[int]:
        """Ordered list of floors this lift will visit (for UI)."""
        lift = self.repo.get_lift(lift_id)
        if not lift:
            return []

        floors = sorted(
            {req.floor for req in self.repo.get_pending_request() if req.lift_id == lift_id}
        )
        if not floors:
            return []

        current = lift.current_floor
        direction = lift.direction
        queue: list[int] = []
        remaining = set(floors)

        while remaining:
            if direction == "up":
                ahead = sorted(f for f in remaining if f > current)
                if ahead:
                    target = ahead[0]
                else:
                    direction = "down"
                    continue
            elif direction == "down":
                below = sorted((f for f in remaining if f < current), reverse=True)
                if below:
                    target = below[0]
                else:
                    direction = "up"
                    continue
            else:
                target = min(remaining, key=lambda f: abs(f - current))
                direction = "up" if target > current else "down"

            queue.append(target)
            remaining.remove(target)
            current = target

        return queue

    def get_next_floor_for_lift(self, lift_id: int) -> int | None:
        queue = self.get_scan_queue(lift_id)
        if not queue:
            return None

        lift = self.repo.get_lift(lift_id)
        if not lift:
            return None

        current = lift.current_floor
        for floor in queue:
            if floor != current:
                return floor
        return queue[0] if queue else None

    def update_and_serve(self, lift_id: int) -> None:
        lift = self.repo.get_lift(lift_id)
        if not lift:
            return

        pending = self.repo.get_pending_request()
        at_floor = [
            req
            for req in pending
            if req.lift_id == lift_id and req.floor == lift.current_floor
        ]

        if at_floor:
            self.repo.move_lift(lift_id, lift.current_floor, lift.direction, "open")
            self.repo.log_event(lift_id, "door_opened")
            for req in at_floor:
                self.repo.mark_served(req.request_id)
                self.repo.log_event(lift_id, "lift_arrived")
            self.repo.move_lift(lift_id, lift.current_floor, lift.direction, "closed")
            self.repo.log_event(lift_id, "door_closed")
            lift = self.repo.get_lift(lift_id)

        next_floor = self.get_next_floor_for_lift(lift_id)
        if next_floor is None:
            if lift.direction != "idle":
                self.repo.move_lift(lift_id, lift.current_floor, "idle", "closed")
            return

        if next_floor > lift.current_floor:
            new_floor = lift.current_floor + 1
            new_direction = "up"
        elif next_floor < lift.current_floor:
            new_floor = lift.current_floor - 1
            new_direction = "down"
        else:
            return

        self.repo.move_lift(lift_id, new_floor, new_direction, "closed")
