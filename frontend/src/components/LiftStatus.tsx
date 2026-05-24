import { useEffect, useState } from "react"
import { getNextFloor } from "../services/api";

const LiftStatus = ({ lift_id }: { lift_id: number }) => {
  const [nextfloor, setNextfloor] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchnext = async () => {
    setLoading(true);
    try {
      const data = await getNextFloor(lift_id);
      // assuming backend returns { next_floor: number }
      setNextfloor(data.next_floor);
      setError(null);
    } catch (err) {
      setError("Failed to fetch next floor");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchnext();
    const pollInterval = setInterval(() => {
      fetchnext();
    }, 3000);
    return () => clearInterval(pollInterval);
  }, [lift_id]);

  return (
    <div className="assign-lift">
      <h3>Lift {lift_id} Status</h3>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {nextfloor !== null && !loading && !error && (
        <p>Next floor: {nextfloor}</p>
      )}
    </div>
  );
};

export default LiftStatus;
