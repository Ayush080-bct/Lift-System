import { LiftsList } from "./components/LiftsList";
import { RequestPanel } from "./components/RequestPanel";

const App=()=>{
  return(
    <>
      <header>Lift System</header>
      <LiftsList />
      <RequestPanel />
    </>
  )
}
export default App;