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

-- ============= INSERT QUERIES =============
-- Insert a new lift request
-- This query creates a new lift request entry and returns the generated request_id
INSERT INTO requests (floor, status)
VALUES (5, 'pending')
RETURNING request_id;

-- ============= UPDATE QUERIES =============
-- Update lift position and status
-- This query updates the lift's current floor, direction, and door status
UPDATE lifts SET current_floor=2, direction='up', door_status='open' WHERE lift_id=3;