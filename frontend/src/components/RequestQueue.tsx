import { getRequests } from "../services/api";
import { useState,useEffect } from "react";
import type { Request } from "../types";

export function RequestQueue(){
    const [request,setRequest]=useState<Request[]>([])
    const [loading,setLoading]=useState(false)
    const [error,setError]=useState("")

    const fetchRequest=async ()=>{
        setLoading(true)
        try{
            const data=await getRequests();
            setRequest(data);
        }catch (err){
            setError("Failed to fetch Requests")
        }finally{
            setLoading(false);
        }
    }
    useEffect(()=>{
        // Fetch immediately on mount
        fetchRequest();
        
        // Poll every 3 seconds for new requests
        const pollInterval=setInterval(()=>{
            fetchRequest();
        }, 3000);
        
        // Clean up interval on unmount
        return ()=>clearInterval(pollInterval);
    },[]);
//     User is on Dashboard (component is mounted)
// User clicks to go to another page
// RequestQueue component is removed
// Cleanup function runs → timer stops ✅
// No more polling in the background

// Mount: RequestQueue appears on Dashboard → immediately fetch requests + start 3s polling
// Unmount: User leaves Dashboard → stop the polling timer
    return(
        <div className="request_que">
            <h2>Pending Requests</h2>
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            <table cellPadding={2} cellSpacing={5}>
                <thead>
                    <tr>
                        <th>Id</th>
                        <th>Floor</th>
                        <th>Lift_id</th>
                        <th>Status</th>
                        <th>TimeRequested</th>
                    </tr>

                </thead>
                <tbody>
                    {request.map(req=>(
                        <tr key={req.request_id}>
                            <td>{req.request_id}</td>
                            <td>{req.floor}</td>
                            <td>{req.lift_id ? String(req.lift_id):"Not assigned"}</td>
                            <td>{req.status}</td>
                            <td>{new Date(req.request_time).toLocaleTimeString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )

}