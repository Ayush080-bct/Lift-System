import type { Log } from "../types";
import { useState, useEffect } from "react";
import { getLogs } from "../services/api";

const EVENT_LABELS: Record<string, string> = {
  button_pressed: "Button pressed",
  lift_arrived: "Arrived",
  door_opened: "Door opened",
  door_closed: "Door closed",
  emergency_stop: "Emergency",
};

export function LogViewer() {
  const [logs, setLogs] = useState<Log[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLog = async () => {
      try {
        setLogs(await getLogs());
        setError(null);
      } catch {
        setError("Failed to fetch logs");
      }
    };
    fetchLog();
    const interval = setInterval(fetchLog, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="log-viewer">
      <h2>Event logs</h2>
      {error && <p>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Lift</th>
            <th>Event</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {logs.slice(0, 20).map((log) => (
            <tr key={log.log_id}>
              <td>{log.lift_id}</td>
              <td>{EVENT_LABELS[log.event_type] ?? log.event_type}</td>
              <td>{new Date(log.event_time).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
