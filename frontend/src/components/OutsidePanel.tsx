import { useState } from "react";
import { createRequest } from "../services/api";
import "../styles/OutsidePanel.css";

interface Props {
    onRequestCreated: () => void;
}

export function OutsidePanel({ onRequestCreated }: Props) {
    const [message, setMessage] = useState<string | null>(null);

    const handleCallLift = async (direction: "up" | "down") => {
        // For now, just log - in future this would call from outside
        // For demonstration, request floor based on direction
        const floor = direction === "up" ? 5 : 3;
        try {
            const result = await createRequest(floor, 1);
            setMessage(`${direction.toUpperCase()} called! Floor ${result.floor}`);
            setTimeout(() => setMessage(null), 3000);
            onRequestCreated();
        } catch (err) {
            setMessage("Failed to call lift");
        }
    };

    return (
        <div className="outside-panel">
            <h3>Outside - Call Lift</h3>
            <div className="direction-buttons">
                <button
                    className="direction-btn up-btn"
                    onClick={() => handleCallLift("up")}
                >
                    ⬆️ UP
                </button>
                <button
                    className="direction-btn down-btn"
                    onClick={() => handleCallLift("down")}
                >
                    ⬇️ DOWN
                </button>
            </div>
            {message && <div className="message outside-message">{message}</div>}
        </div>
    );
}
