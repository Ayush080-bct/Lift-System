import type { Lift } from "../types";
import "../styles/LiftVisualization.css";

interface Props {
  lift: Lift;
  queue?: number[];
}

const TOTAL_FLOORS = 10;

export function LiftVisualization({ lift, queue = [] }: Props) {
  const arrow = lift.direction === "up" ? "↑" : lift.direction === "down" ? "↓" : "-";
  const dirClass =
    lift.direction === "up" ? "dir-up" : lift.direction === "down" ? "dir-down" : "dir-idle";

  const carBottom = ((lift.current_floor - 1) / (TOTAL_FLOORS - 1)) * 100;

  return (
    <div className="lift-shaft">
      <div className="lift-shaft__header">
        <h2>Lift {lift.lift_id}</h2>
        <div className={`floor-display ${dirClass}`}>
          <span className="floor-display__num">{lift.current_floor}</span>
          <span className="floor-display__arrow">{arrow}</span>
        </div>
      </div>

      <div className="shaft">
        <div className="shaft__labels">
          {Array.from({ length: TOTAL_FLOORS }, (_, i) => TOTAL_FLOORS - i).map((f) => (
            <div key={f} className="shaft__label-row">
              <span>{f}</span>
              {queue.includes(f) && lift.current_floor !== f && (
                <span className="shaft__stop-dot" title="Stop scheduled" />
              )}
            </div>
          ))}
        </div>

        <div className="shaft__track">
          <div
            className={`lift-car ${lift.door_status === "open" ? "lift-car--doors-open" : ""}`}
            style={{ bottom: `${carBottom}%` }}
          >
            <div className="lift-car__door lift-car__door--left" />
            <div className="lift-car__door lift-car__door--right" />
          </div>
        </div>
      </div>

      <div className="lift-shaft__meta">
        <span className={dirClass}>{lift.direction}</span>
        <span> | </span>
        <span>Doors {lift.door_status}</span>
        {queue.length > 0 && (
          <>
            <span> | </span>
            <span className="lift-shaft__queue">Next: {queue.join(", ")}</span>
          </>
        )}
      </div>
    </div>
  );
}
