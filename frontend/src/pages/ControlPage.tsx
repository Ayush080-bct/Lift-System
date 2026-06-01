import { getAllLifts, getRequests, simulateLiftStep } from "../services/api";
import { useState, useEffect } from "react";
import type { Lift, Request } from "../types";
import { LiftVisualization } from "../components/LiftVisualization";
import { InsidePanel } from "../components/InsidePanel";
import { OutsidePanel } from "../components/OutsidePanel";
import { RequestTable } from "../components/RequestTable";
import "./ControlPage.css";

const ControlPage = () => {
    const [lift, setLift] = useState<Lift | null>(null);
    const [requests, setRequests] = useState<Request[]>([]);
    const [loading, setLoading] = useState(false);

    // Fetch lift status and requests, and simulate lift movement
    useEffect(() => {
        const fetchData = async () => {
            try {
                const lifts = await getAllLifts();
                if (lifts.length > 0) {
                    setLift(lifts[0]); // Get lift 1
                    // Simulate one step of lift movement for each lift
                    await simulateLiftStep(lifts[0].lift_id);
                }
                const reqs = await getRequests();
                setRequests(reqs);
            } catch (err) {
                console.error("Failed to fetch data", err);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 2000); // Poll every 2 seconds and simulate movement
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="control-page">
            <header className="control-header">
                <h1>🛗 Lift Control System</h1>
            </header>

            <div className="control-container">
                {/* LEFT SIDE: Lift Animation + Outside Buttons */}
                <div className="left-section">
                    <LiftVisualization lift={lift} />
                    <OutsidePanel onRequestCreated={() => setLoading(!loading)} />
                </div>

                {/* RIGHT SIDE: Inside Buttons + Request Table */}
                <div className="right-section">
                    <InsidePanel
                        loading={loading}
                        onRequestCreated={() => setLoading(!loading)}
                    />
                    <RequestTable requests={requests} />
                </div>
            </div>
        </div>
    );
};

export default ControlPage;