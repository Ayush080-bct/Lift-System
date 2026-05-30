import type { Log } from "../types";
import { useState, useEffect } from "react";
import { getLogs } from "../services/api";

export function LogViewer() {
    const [logs, setLogs] = useState<Log[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchLog = async () => {
            setLoading(true);
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
        const pollInterval=setInterval(()=>{
            fetchLog();
        },3000);
        return ()=>clearInterval(pollInterval);
    }, []);

    return (
        <div className="log-viewer">
            <h2>Event Logs</h2>
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
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
                    {logs.slice(-20).map(log => (
                        <tr key={log.log_id}>
                            <td>{log.log_id}</td>
                            <td>{log.lift_id ? String(log.lift_id) : "Not assigned"}</td>
                            <td>{log.event_type}</td>
                            <td>{new Date(log.event_time).toLocaleTimeString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}