import type { Log } from "../types";
import { useState, useEffect } from "react";
import { getLogs } from "../services/api";
import "./styles/LogViewer.css";

export function LogViewer() {
    const [logs, setLogs] = useState<Log[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchLog = async () => {
            try {
                const data = await getLogs();
                setLogs(data);
            } catch (err) {
                setError("Failed to fetch logs");
            } finally {
                setLoading(false);
            }
        };
        fetchLog();
    }, []);

    return (
        <div className="log-viewer">
            <h2>📊 Event Logs</h2>
            
            {loading && (
                <div className="skeleton-card">
                    <div className="skeleton" style={{height: '30px'}}></div>
                    <div className="skeleton" style={{height: '120px', marginTop: '15px'}}></div>
                </div>
            )}
            
            {error && (
                <div className="empty-state">
                    <div className="empty-state-icon">⚠️</div>
                    <p className="empty-state-message">{error}</p>
                </div>
            )}
            
            {!loading && !error && logs.length === 0 && (
                <div className="empty-state">
                    <div className="empty-state-icon">📝</div>
                    <p className="empty-state-message">No logs yet. Request a lift to see events!</p>
                </div>
            )}
            
            {logs.length > 0 && (
                <table cellPadding={2} cellSpacing={5}>
                    <thead>
                        <tr>
                            <th>Log ID</th>
                            <th>Lift ID</th>
                            <th>Event Type</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logs.slice().reverse().map(log => (
                            <tr key={log.log_id}>
                                <td>#{log.log_id}</td>
                                <td><strong>Lift {log.lift_id ?String(log.lift_id):"Not assigned" }</strong></td>
                                <td><span className="event-badge">{log.event_type}</span></td>
                                <td>{new Date(log.event_time).toLocaleTimeString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}