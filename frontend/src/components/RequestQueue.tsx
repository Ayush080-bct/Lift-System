import { useState,useEffect } from "react";
import { getRequests, serveRequest } from "../services/api";
import type { Request } from "../types";
import "./styles/RequestQueue.css";

export function RequestQueue(){
    const [requests,setRequests]=useState<Request[]>([]);
    const [loading,setLoading]=useState(false);
    const [error,setError]=useState<string | null>(null);
    const [servingId,setServingId]=useState<number | null>(null);

    const fetchRequests=async ()=>{
        try{
            const data=await getRequests();
            setRequests(data);
        }catch (err){
            setError("Failed to fetch request")
        }finally {
            setLoading(false);
        }
    };

    useEffect(()=>{
        fetchRequests();
    },[]);

    const handleServe=async(requestId: number)=>{
        setServingId(requestId);
        try{
            await serveRequest(requestId);
            // Refresh requests after serving
            await fetchRequests();
        }catch(err){
            console.error("Failed to serve request");
        }finally{
            setServingId(null);
        }
    };

    return (
        <div className="request-queue">
            <h2>📋 Pending Requests</h2>
            
            {loading && (
                <div className="skeleton-card">
                    <div className="skeleton" style={{height: '30px'}}></div>
                    <div className="skeleton" style={{height: '100px', marginTop: '15px'}}></div>
                </div>
            )}
            
            {error && (
                <div className="empty-state">
                    <div className="empty-state-icon">⚠️</div>
                    <p className="empty-state-message">{error}</p>
                </div>
            )}
            
            {!loading && !error && requests.length === 0 && (
                <div className="empty-state">
                    <div className="empty-state-icon">✅</div>
                    <p className="empty-state-message">No pending requests</p>
                </div>
            )}
            
            {requests.length > 0 && (
                <table cellPadding={2} cellSpacing={5}>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Floor</th>
                            <th>Lift</th>
                            <th>Status</th>
                            <th>Time Requested</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {requests.map(req=>(
                            <tr key={req.request_id}>
                                <td>#{req.request_id}</td>
                                <td><strong>{req.floor}</strong></td>
                                <td>{req.lift_id ? String(req.lift_id) : "Not assigned"}</td>
                                <td>
                                    <span className={`status status-${req.status}`}>
                                        {req.status === 'pending' ? '⏳ Pending' : '✅ Served'}
                                    </span>
                                </td>
                                <td>{new Date(req.request_time).toLocaleTimeString()}</td>
                                <td>
                                    {req.status === 'pending' && (
                                        <button 
                                            className="serve-btn"
                                            onClick={()=>handleServe(req.request_id)}
                                            disabled={servingId === req.request_id}
                                        >
                                            {servingId === req.request_id ? '⏳...' : '✅ Serve'}
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    )
}
