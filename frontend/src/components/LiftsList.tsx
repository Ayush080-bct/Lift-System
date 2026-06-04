import { getAllLifts } from "../services/api";
import { useState, useEffect } from "react";
import type { Lift } from "../types";
import { LiftCard } from "./LiftCard";

export function LiftsList() {
  const [lifts, setLifts] = useState<Lift[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLifts = async () => {
      try {
        setLifts(await getAllLifts());
        setError(null);
      } catch {
        setError("Failed to fetch lifts");
      } finally {
        setLoading(false);
      }
    };

    fetchLifts();
    const interval = setInterval(fetchLifts, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="lifts-list">
      <h2>All lifts</h2>
      {loading && <p>Loading…</p>}
      {error && <p>{error}</p>}
      <div className="lifts-list__grid">
        {lifts.map((lift) => (
          <LiftCard key={lift.lift_id} lift={lift} />
        ))}
      </div>
    </div>
  );
}
