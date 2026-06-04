import { useState, useEffect, useCallback } from "react";
import { getNextFloor, getLift } from "../services/api";
import type { Lift } from "../types";

export default function LiftStatus({ liftId }: { liftId: number }) {
  const [lift, setLift] = useState<Lift | null>(null);
  const [nextFloor, setNextFloor] = useState<number | null>(null);
  const [queue, setQueue] = useState<number[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchLiftData = useCallback(async () => {
    try {
      const [liftData, nextData] = await Promise.all([getLift(liftId), getNextFloor(liftId)]);
      setLift(liftData);
      setNextFloor(nextData.next_floor);
      setQueue(nextData.queue ?? []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch");
    }
  }, [liftId]);

  useEffect(() => {
    fetchLiftData();
    const interval = setInterval(fetchLiftData, 2000);
    return () => clearInterval(interval);
  }, [fetchLiftData]);

  if (error) return <div className="lift-status-card lift-status-card--error">{error}</div>;
  if (!lift) return <div className="lift-status-card">Loading…</div>;

  return (
    <div className="lift-status-card">
      <h3>Lift {lift.lift_id}</h3>
      <p>Floor {lift.current_floor}</p>
      <p>{lift.direction} · {lift.door_status}</p>
      <p>Next: {nextFloor ?? "—"}</p>
      {queue.length > 0 && <p className="lift-status-card__queue">{queue.join(" → ")}</p>}
    </div>
  );
}
