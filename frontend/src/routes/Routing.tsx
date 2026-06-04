import ControlPage from "../pages/ControlPage";
import DashboardPage from "../pages/DashboardPage";
import { BrowserRouter, Routes, Route } from "react-router-dom";

const Routing = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<ControlPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
    </Routes>
  </BrowserRouter>
);

export default Routing;
