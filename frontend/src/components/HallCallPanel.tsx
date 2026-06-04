import { useState } from "react";
import { createRequest } from "../services/api";
import "../styles/HallCallPanel.css";

interface Props {
  onRequestCreated: () => void;
}

const FLOORS = Array.from({ length: 10 }, (_, i) => 10 - i);

export function HallCallPanel({ onRequestCreated }: Props) {
  const [message, setMessage] = useState<string | null>(null);
  const [loadingFloor, setLoadingFloor] = useState<number | null>(null);

  const callLift = async (floor: number, direction: "up" | "down") => {
    setLoadingFloor(floor);
    try {
      await createRequest(floor);
      setMessage(`Floor ${floor} — ${direction.toUpperCase()} call sent`);
      setTimeout(() => setMessage(null), 2500);
      onRequestCreated();
    } catch {
      setMessage("Call failed — is the backend running?");
      setTimeout(() => setMessage(null), 3000);
    } finally {
      setLoadingFloor(null);
    }
  };

  return (
    <div className="hall-panel">
      <h3 className="hall-panel__title">Hall calls</h3>
      <p className="hall-panel__hint">Press UP or DOWN at any floor</p>
      <div className="hall-panel__list">
        {FLOORS.map((floor) => (
          <div key={floor} className="hall-panel__row">
            <span className="hall-panel__floor-label">{floor}</span>
            <button
              type="button"
              className="hall-btn hall-btn--up"
              disabled={loadingFloor === floor || floor === 10}
              onClick={() => callLift(floor, "up")}
              aria-label={`Call lift up from floor ${floor}`}
            >
              ▲
            </button>
            <button
              type="button"
              className="hall-btn hall-btn--down"
              disabled={loadingFloor === floor || floor === 1}
              onClick={() => callLift(floor, "down")}
              aria-label={`Call lift down from floor ${floor}`}
            >
              ▼
            </button>
          </div>
        ))}
      </div>
      {message && <p className="hall-panel__message">{message}</p>}
    </div>
  );
}
