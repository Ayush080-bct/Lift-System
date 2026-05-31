import { useState } from "react";
import { createRequest } from "../services/api";
import "../styles/InsidePanel.css";

interface Props {
    loading: boolean;
    onRequestCreated: () => void;
}

export function InsidePanel({ loading, onRequestCreated }: Props) {
    const [selectedFloor, setSelectedFloor] = useState<number | null>(null);
    const [message, setMessage] = useState<string | null>(null);

    const floorButtons = Array.from({ length: 10 }, (_, i) => i + 1);

    const handleFloorRequest = async (floor: number) => {
        setSelectedFloor(floor);
        try {
            const result = await createRequest(floor, 1); // lift_id = 1
            setMessage(`Request created: Floor ${result.floor}, Lift 1`);
            setTimeout(() => setMessage(null), 3000);
            onRequestCreated();
        } catch (err) {
            setMessage("Failed to create request");
        }
    };

    return (
        <div className="inside-lift-panel">
            <h3>Inside Lift - Select Floor</h3>
            <div className="floor-buttons">
                {floorButtons.reverse().map((floor) => (
                    <button
                        key={floor}
                        onClick={() => handleFloorRequest(floor)}
                        disabled={loading || selectedFloor === floor}
                        className={`floor-btn ${selectedFloor === floor ? "active" : ""}`}
                    >
                        {floor}
                    </button>
                ))}
            </div>
            {message && <div className="message">{message}</div>}
        </div>
    );
}
