import { useState } from "react";
import { createRequest } from "../services/api";
import "../styles/OutsidePanel.css";

interface Props {
    floor: number;  // ✅ ADDED: Which floor this panel is on
    onRequestCreated: () => void;
}

export function OutsidePanel({ floor, onRequestCreated }: Props) {
    const [message, setMessage] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleCallLift = async (direction: "up" | "down") => {
        setLoading(true);
        try {
            // ✅ FIXED: Use actual floor, not hardcoded
            await createRequest(floor);
            setMessage(`${direction.toUpperCase()} called from Floor ${floor}`);
            setTimeout(() => setMessage(null), 3000);
            onRequestCreated();
        } catch (err) {
            setMessage("Failed to call lift");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="outside-panel">
            <h3>Floor {floor}</h3>
            <div className="direction-buttons">
                <button
                    className="direction-btn up-btn"
                    onClick={() => handleCallLift("up")}
                    disabled={loading || floor === 10}  // Can't go up from top floor
                >
                    ⬆️ UP
                </button>
                <button
                    className="direction-btn down-btn"
                    onClick={() => handleCallLift("down")}
                    disabled={loading || floor === 1}  // Can't go down from ground floor
                >
                    ⬇️ DOWN
                </button>
            </div>
            {message && <div className="message outside-message">{message}</div>}
        </div>
    );
}