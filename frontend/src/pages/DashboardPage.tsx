import { LogViewer } from "../components/LogViewer";
import { LiftsList } from "../components/LiftsList";

import { RequestQueue } from "../components/RequestQueue";
import LiftStatus from "../components/LiftStatus";

const DashboardPage=()=>{
    return(
        <>
        <header className="app-header">Lift Tracking Dashboard</header>
        <LiftsList />
        
        <RequestQueue />
        {[1,2,3].map(id => (
  <LiftStatus key={id} lift_id={id} />
))}
        <LogViewer />
        </>
    )
}
export default DashboardPage;