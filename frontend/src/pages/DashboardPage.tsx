import { LogViewer } from "../components/LogViewer";
import { LiftsList } from "../components/LiftsList";
import { RequestQueue } from "../components/RequestQueue";
import "./DashboardPage.css";
import "../styles/Dashboard.css";

const DashboardPage = () => (
  <div className="dashboard-page">
    <header className="dashboard-header">
      <h1>Lift Dashboard</h1>
      <nav>
        <a href="/">Control</a>
        <a href="/dashboard">Dashboard</a>
      </nav>
    </header>
    <LiftsList />
    <RequestQueue />
    <LogViewer />
  </div>
);

export default DashboardPage;
