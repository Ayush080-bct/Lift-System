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

INSERT INTO requests (floor, status)--specifies which columns you’re inserting values into.
VALUES (5, 'pending')
RETURNING request_id;-- tells PostgreSQL to immediately give back the newly generated request_id (since it’s a SERIAL primary key).

UPDATE lifts SET current_floor=2, direction=up, door_status=open where lift_id=3;