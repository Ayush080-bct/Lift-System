import { useState, useEffect, useCallback } from "react";
import { getAllLifts, getRequests, getNextFloor } from "../services/api";
import type { Lift, Request } from "../types";
import { LiftVisualization } from "../components/LiftVisualization";
import { InsidePanel } from "../components/InsidePanel";
import { HallCallPanel } from "../components/HallCallPanel";
import { RequestTable } from "../components/RequestTable";
import "./ControlPage.css";

/** Phase 1: single animated lift. When scaling, change activeLiftId to switch the shaft view. */
const DEFAULT_LIFT_ID = 1;
const POLL_MS = 2000;

const ControlPage = () => {
  const [lifts, setLifts] = useState<Lift[]>([]);
  const [requests, setRequests] = useState<Request[]>([]);
  const [queue, setQueue] = useState<number[]>([]);
  const [activeLiftId, setActiveLiftId] = useState(DEFAULT_LIFT_ID);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const [liftsData, reqsData] = await Promise.all([getAllLifts(), getRequests()]);
      setLifts(liftsData);
      setRequests(reqsData);
      setError(null);

      const id = liftsData.some((l) => l.lift_id === activeLiftId)
        ? activeLiftId
        : liftsData[0]?.lift_id ?? DEFAULT_LIFT_ID;

      if (id !== activeLiftId && liftsData.length) {
        setActiveLiftId(id);
      }

      if (id) {
        const next = await getNextFloor(id);
        setQueue(next.queue ?? []);
      }
    } catch {
      setError("Cannot reach backend — start FastAPI on port 8000");
    }
  }, [activeLiftId]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, POLL_MS);
    return () => clearInterval(interval);
  }, [fetchData]);

  const activeLift = lifts.find((l) => l.lift_id === activeLiftId) ?? lifts[0];

  return (
    <div className="control-page">
      <header className="control-header">
        <h1>Lift Control</h1>
        <p>Floor requests use SCAN. Lift moves every 2 seconds.</p>
        <nav className="control-nav">
          <a href="/">Control</a>
          <a href="/dashboard">Dashboard</a>
        </nav>
      </header>

      {error && <p className="control-error">{error}</p>}

      {/* When you add more lifts: compact chips switch which one is animated */}
      {lifts.length > 1 && (
        <div className="lift-selector">
          {lifts.map((l) => (
            <button
              key={l.lift_id}
              type="button"
              className={`lift-selector__chip ${l.lift_id === activeLiftId ? "lift-selector__chip--active" : ""}`}
              onClick={() => setActiveLiftId(l.lift_id)}
            >
              Lift {l.lift_id} · F{l.current_floor} {l.direction !== "idle" ? (l.direction === "up" ? "↑" : "↓") : ""}
            </button>
          ))}
        </div>
      )}

      <div className="control-layout">
        <section className="control-shaft-zone">
          {activeLift ? (
            <div className="shaft-row">
              <HallCallPanel onRequestCreated={fetchData} />
              <LiftVisualization lift={activeLift} queue={queue} />
            </div>
          ) : (
            <p className="control-loading">Loading lift…</p>
          )}
        </section>

        <aside className="control-side">
          {activeLift && (
            <InsidePanel
              currentFloor={activeLift.current_floor}
              onRequestCreated={fetchData}
            />
          )}
          <RequestTable requests={requests} />
        </aside>
      </div>
    </div>
  );
};

export default ControlPage;
