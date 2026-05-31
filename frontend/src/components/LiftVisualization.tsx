import type { Lift } from "../types";
import "../styles/LiftVisualization.css";

interface Props {
    lift: Lift | null;
}

export function LiftVisualization({ lift }: Props) {
    const floorButtons = Array.from({ length: 10 }, (_, i) => i + 1);

    return (
        <div className="lift-shaft">
            <h2>Lift 1 Status</h2>
            <div className="shaft-visualization">
                {/* Floor indicators */}
                <div className="floors">
                    {floorButtons.reverse().map((floor) => (
                        <div key={floor} className="floor-indicator">
                            <span className="floor-number">Floor {floor}</span>
                            {lift && lift.current_floor === floor && (
                                <div className="lift-box">
                                    <div className="lift-car">
                                        <div className="door">🚪</div>
                                        <div className="door">🚪</div>
                                    </div>
                                    {lift.door_status === "open" && (
                                        <span className="door-status">Doors OPEN</span>
                                    )}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Current Status */}
            <div className="lift-status">
                <p>
                    <strong>Current Floor:</strong> {lift?.current_floor}
                </p>
                <p>
                    <strong>Direction:</strong> {lift?.direction?.toUpperCase()}
                </p>
                <p>
                    <strong>Door Status:</strong> {lift?.door_status?.toUpperCase()}
                </p>
            </div>
        </div>
    );
}
