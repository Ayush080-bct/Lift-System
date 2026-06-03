import type { Lift } from "../types";

interface LiftCardProps {
  lift: Lift;
}

export function LiftCard({ lift }: LiftCardProps) {
  return (
    <div className="lift-card">
      <h3>Lift {lift.lift_id}</h3>
      <p>Floor: {lift.current_floor}</p>
      <p>Direction: {lift.direction}</p>
      <p>Doors: {lift.door_status}</p>
    </div>
  );
}
