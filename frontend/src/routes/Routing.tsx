import ControlPage from "../pages/ControlPage";
import DashboardPage from "../pages/DashboardPage";
import { BrowserRouter,Routes,Route } from "react-router-dom";
const Routing=()=>{
    return(
    <BrowserRouter>
    <Routes>
        <Route path='/' element={<ControlPage />} />
        <Route path='/Dashboard' element={<DashboardPage />} />
    </Routes>
    </BrowserRouter>
    )
}
export default Routing;