import React, { useState} from "react";
import { createRequest } from "../services/api";
import "./styles/RequestPanel.css";

export function RequestPanel(){
    const [floor,setFloor]=useState("");
    const [loading,setLoading]=useState(false);
    const [message,setMessage]=useState<{type: 'success'|'error', text: string} | null>(null);

    const handleSubmit=async (e:React.FormEvent)=>{
        e.preventDefault();
        
        if(!floor || Number(floor) < 0){
            setMessage({type: 'error', text: 'Please enter a valid floor number'});
            return;
        }

        setLoading(true);
        setMessage(null);

        try{
            const result=await createRequest(Number(floor));
            setMessage({
                type: 'success', 
                text: `✅ Request created for floor ${floor}!`
            });
            setFloor("");
        }catch (err){
            setMessage({
                type: 'error',
                text: '❌ Failed to create request. Is the backend running?'
            });
        }finally {
            setLoading(false);
        }
    };
    
    return(
        <div className="request-panel">
            <h2>🛗 Request Lift</h2>
            <form onSubmit={handleSubmit}>
                <input 
                    type="number"
                    value={floor}
                    onChange={(e)=>setFloor(e.target.value)}
                    placeholder="Enter floor number (0-10)"
                    min="0"
                    max="10"
                    required
                />
                <button type='submit' disabled={loading}>
                    {loading ? "⏳ Requesting....":"📍 Request Lift"}
                </button>
            </form>
            {message && (
                <div className={`message message-${message.type}`}>
                    {message.text}
                </div>
            )}
        </div>
    )
}