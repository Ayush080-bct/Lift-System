import { useState,useEffect } from "react";
import { getRequests } from "../services/api";
import type { Request } from "../types";

export function RequestQueue(){
    const [requests,setRequests]=useState<Request[]>([]);
    const [loading,setLoading]=useState(false);
    const [error,setError]=useState<string | null>(null);

    useEffect(()=>{
        const fetchrequests=async ()=>{
            try{
                const data=await getRequests();
                setRequests(data);
            }catch (err){
                setError("Failed to fetch request")
            }finally {
                setLoading(false);
            }
        };
        fetchrequests();
    },[]);

    return (
        <div className="request-queue">
            <h2>Pending requests</h2>
            {loading && <p>Loading....</p>}
            {error && <p>{error}</p>}
            <table cellPadding={2} cellSpacing={5}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Floor</th>
                        <th>Lift</th>
                        <th>Status</th>
                        <th>Time Requested</th>
                    </tr>
                </thead>
                <tbody>
                    {requests.map(req=>(
                        <tr key={req.request_id}>
                            <td>{req.request_id}</td>
                            <td>{req.floor}</td>
                            <td>{req.lift_id ? String(req.lift_id) : "Not assigned"}</td>
                            <td>{req.status}</td>
                            <td>{new Date(req.request_time).toLocaleTimeString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}