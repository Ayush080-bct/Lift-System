"""
Lift Scheduling Service - SCAN Algorithm
Lifts move in one direction until all requests in that direction are served,
then reverse direction. This minimizes travel time and is energy efficient.
"""

from backend.repository.repository import LiftRepository

class SchedulingService:
    def __init__(self, repo: LiftRepository):
        self.repo = repo
    
    def assign_lift_to_request(self, requested_floor: int):
        """
        Assign best lift to handle a request using SCAN algorithm.
        
        Algorithm:
        1. Find lifts moving toward the requested floor
        2. Pick the one closest to requested floor
        3. If no lift moving toward it, pick closest idle lift
        4. If no idle lift, pick the one that will reach it first
        """
        lifts = self.repo.get_all_lifts()
        pending_requests = self.repo.get_pending_request()
        
        if not lifts:
            return None
        
        # Count pending requests for each lift
        lift_load = {lift.lift_id: 0 for lift in lifts}
        for req in pending_requests:
            if req.lift_id:
                lift_load[req.lift_id] += 1
        
        # Find best lift
        best_lift = None
        best_score = float('inf')
        
        for lift in lifts:
            # Skip overloaded lifts (more than 5 pending requests)
            if lift_load[lift.lift_id] > 5:
                continue
            
            # Priority 1: Lift moving toward requested floor (SCAN algorithm)
            if lift.direction == "up" and lift.current_floor < requested_floor:
                distance = requested_floor - lift.current_floor
                score = distance + (lift_load[lift.lift_id] * 2)
                if score < best_score:
                    best_score = score
                    best_lift = lift
            
            elif lift.direction == "down" and lift.current_floor > requested_floor:
                distance = lift.current_floor - requested_floor
                score = distance + (lift_load[lift.lift_id] * 2)
                if score < best_score:
                    best_score = score
                    best_lift = lift
            
            # Priority 2: Idle lift
            elif lift.direction == "idle":
                distance = abs(lift.current_floor - requested_floor)
                score = distance + (lift_load[lift.lift_id] * 2)
                if score < best_score:
                    best_score = score
                    best_lift = lift
        
        # If no lift found, fallback to closest lift regardless of direction
        if best_lift is None:
            best_lift = min(lifts, key=lambda l: abs(l.current_floor - requested_floor))
        
        return best_lift.lift_id if best_lift else None
    
    def get_next_floor_for_lift(self, lift_id: int):
        """
        Get the next floor a lift should visit based on pending requests
        and SCAN algorithm logic.
        """
        lift = self.repo.get_lift(lift_id)
        pending_requests = self.repo.get_pending_request()
        
        # Filter requests for this lift
        lift_requests = [req for req in pending_requests if req.lift_id == lift_id]
        
        if not lift_requests:
            # No pending requests, go to idle state
            return None
        
        # Get all unique floors for this lift
        floors = sorted(set(req.floor for req in lift_requests))
        current_floor = lift.current_floor
        
        # SCAN algorithm: continue in current direction
        if lift.direction == "up":
            # Find floors above current position
            floors_above = [f for f in floors if f > current_floor]
            if floors_above:
                return min(floors_above)  # Go to closest floor above
            else:
                # No floors above, reverse to down
                return max(floors)  # Go to topmost floor first
        
        elif lift.direction == "down":
            # Find floors below current position
            floors_below = [f for f in floors if f < current_floor]
            if floors_below:
                return max(floors_below)  # Go to closest floor below
            else:
                # No floors below, reverse to up
                return min(floors)  # Go to bottom floor first
        
        else:  # idle
            # Pick closest floor
            return min(floors, key=lambda f: abs(f - current_floor))
