-- ============= LIFT QUERIES =============
-- Get lift status
SELECT lift_id, current_floor, direction, door_status FROM lifts WHERE lift_id = 1;

-- Get all lifts
SELECT * FROM lifts;

-- ============= REQUEST QUERIES =============
-- Get pending requests
SELECT * FROM requests WHERE status = 'pending';

-- Get requests for a specific lift
SELECT * FROM requests WHERE lift_id = 1 AND status = 'pending';

-- ============= LOG QUERIES =============
-- Get recent logs
SELECT * FROM logs ORDER BY event_time DESC LIMIT 10;