import { getAllLifts } from "../services/api";
import { useState,useEffect } from "react";
import type { Lift } from "../types";
import { LiftCard } from "./LiftCard";
import "./styles/LiftsList.css";

export function LiftsList(){
    const [lifts,setLifts]=useState<Lift[]>([])
    const [loading,setLoading]=useState(true);
    const [error,setError]=useState<string | null>(null);

    useEffect(()=>{// useEffect is used to handle side effects like API calls,
// timers, and event listeners after component rendering.
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
        fetchLifts();
    },[]);//dependency array [],without it it works same like , when we dont use sideeffect 
    //i.e with each render it will run fetch which intialize request each time
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