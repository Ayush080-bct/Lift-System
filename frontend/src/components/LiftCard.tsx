import type { Lift } from "../types";


interface LiftCardProps {
    lift: Lift;
}

export function LiftCard({ lift }: LiftCardProps) {
    
    const getDirectionColor = (direction: string): string => {
        if (direction === "up") return "#4CAF50";    
        if (direction === "down") return "#f44336";    
        if (direction === "idle") return "#FFC107";    
        return "#757575";                             
    };
    const getDirectionEmoji = (direction: string): string => {
        if (direction === "up") return "⬆️";
        if (direction === "down") return "⬇️";
        if (direction === "idle") return "⏸️";
        return "•";
    };

    return (
        <div className="lift-card">
            {/* Header */}
            <div className="card-header">
                <h3>Lift {lift.lift_id}</h3>
                <span className="id-badge">ID: {lift.lift_id}</span>
            </div>

            {/* Floor Display */}
            <div className="floor-section">
                <div className="floor-number">{lift.current_floor}</div>
                <div className="floor-label">Current Floor</div>
            </div>

            {/* Direction Status */}
            <div 
                className="direction-box" 
                style={{ backgroundColor: getDirectionColor(lift.direction) }}
            >
                <span className="direction-emoji">{getDirectionEmoji(lift.direction)}</span>
                <span className="direction-text">{lift.direction.toUpperCase()}</span>
            </div>

            {/* Info Details */}
            <div className="info-grid">
                <div className="info-row">
                    <span className="label">Floor:</span>
                    <span className="value">{lift.current_floor}</span>
                </div>
                <div className="info-row">
                    <span className="label">Door:</span>
                    <span className="value">
                        {lift.door_status === "open" ? "🚪 OPEN" : "🔒 CLOSED"}
                    </span>
                </div>
            </div>

            {/* Status Indicator */}
            <div 
                className="status-dot" 
                style={{ backgroundColor: getDirectionColor(lift.direction) }}
            />
        </div>
    );
}