import type { Request } from "../types";
import "../styles/RequestTable.css";

interface Props {
    requests: Request[];
}

export function RequestTable({ requests }: Props) {
    return (
        <div className="pending-requests">
            <h3>Pending Requests</h3>
            {requests.length === 0 ? (
                <p className="no-requests">No pending requests</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Request ID</th>
                            <th>Floor</th>
                            <th>Lift ID</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {requests.map((req) => (
                            <tr key={req.request_id}>
                                <td>{req.request_id}</td>
                                <td>Floor {req.floor}</td>
                                <td>{req.lift_id ? String(req.lift_id):"-"}</td>
                                <td>
                                    <span className={`status-badge status-${req.status}`}>
                                        {req.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
