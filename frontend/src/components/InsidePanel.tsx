import { useState } from "react";
import { createRequest } from "../services/api";
import "../styles/InsidePanel.css";

interface Props {
  currentFloor: number;
  onRequestCreated: () => void;
}

export function InsidePanel({ currentFloor, onRequestCreated }: Props) {
  const [pressed, setPressed] = useState<Set<number>>(new Set());
  const [message, setMessage] = useState<string | null>(null);

  const floors = Array.from({ length: 10 }, (_, i) => 10 - i);

  const handleFloor = async (floor: number) => {
    if (floor === currentFloor) return;

    setPressed((prev) => new Set(prev).add(floor));
    try {
      await createRequest(floor);
      setMessage(`Floor ${floor} selected`);
      setTimeout(() => setMessage(null), 2000);
      onRequestCreated();
    } catch {
      setMessage("Request failed");
      setPressed((prev) => {
        const next = new Set(prev);
        next.delete(floor);
        return next;
      });
    }
  };

  return (
    <div className="inside-panel">
      <h3 className="inside-panel__title">Inside lift</h3>
      <p className="inside-panel__hint">Select destination floor</p>
      <div className="inside-panel__grid">
        {floors.map((floor) => (
          <button
            key={floor}
            type="button"
            className={`inside-panel__btn ${pressed.has(floor) ? "inside-panel__btn--lit" : ""} ${floor === currentFloor ? "inside-panel__btn--here" : ""}`}
            disabled={floor === currentFloor}
            onClick={() => handleFloor(floor)}
          >
            {floor}
          </button>
        ))}
      </div>
      {message && <p className="inside-panel__message">{message}</p>}
    </div>
  );
}
