import { getAllLifts } from "../services/api";
import { useState,useEffect } from "react";
import type { Lift } from "../types";
import { LiftCard } from "./LiftCard";


export function LiftsList(){
    const [lifts,setLifts]=useState<Lift[]>([])
    const [loading,setLoading]=useState(true);
    const [error,setError]=useState<string | null>(null);

    useEffect(()=>{
        const fetchLifts=async () =>{
            try{
                const data=await getAllLifts();
                setLifts(data);
            }catch(err){
                setError("Failed to fetch Lifts")
            }finally{
                setLoading(false);
            }
        };
        // Fetch immediately on mount
        fetchLifts();
        
        // Poll every 3 seconds for lift updates
        const pollInterval=setInterval(()=>{
            fetchLifts();
        }, 3000);
        
        // Clean up interval on unmount
        return ()=>clearInterval(pollInterval);
    },[]);
    return (
    <div className="lifts-list">
        {loading && <p>Loading Lifts...</p>}
        {error && <p>{error}</p>}
        {lifts.map(lift => (
            <LiftCard key={lift.lift_id} lift={lift} />
        ))}
    </div>
)
}