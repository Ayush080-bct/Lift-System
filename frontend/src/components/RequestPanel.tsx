import React, { useState} from "react";
import { createRequest } from "../services/api";

export function RequestPanel(){
    const [floor,setFloor]=useState("");
    const [loading,setLoading]=useState(false);
    const [message,setMessage]=useState<string | null>(null);

    const handleSubmit=async (e:React.FormEvent)=>{
        e.preventDefault();
        setLoading(true);
        try{
            const result=await createRequest(Number(floor));
            setMessage(`Request Created:${result.message}`);
            setFloor("");
        }catch (err){
            setMessage("Failed to create request");
            
        }finally {
            setLoading(false);
        }
    };
    return(
        <div className="request-panel">
            <h2>Request Lift</h2>
            <form onSubmit={handleSubmit}>
                <input 
                type="number"
                value={floor}
                onChange={(e)=>setFloor(e.target.value)}
                placeholder="Enter floor number"
                required
                />
                <button type='submit' disabled={loading}>
                    {loading ? "Requesting....":"Request Lift"}
                </button>
            </form>
            {message && <p>{message}</p>}
        </div>
    )
}