-- TO RUN SINGLE QUERY SELECT IT AND Click CTRL+E two times


-- ============= LIFT QUERIES =============
-- Get lift status by ID
SELECT lift_id, current_floor, direction, door_status FROM lifts WHERE lift_id = 1;

-- Get all lifts
SELECT * FROM lifts;

-- Update lift position and status
UPDATE lifts SET current_floor=2, direction='up', door_status='open' WHERE lift_id=3;

-- ============= REQUEST QUERIES =============
-- Get all pending requests
SELECT request_id, floor, request_time, status, lift_id FROM requests WHERE status='Pending';

-- Get requests for a specific lift
SELECT * FROM requests WHERE lift_id = 1 AND status = 'pending';

-- Insert a new lift request (returns request_id immediately)
INSERT INTO requests (floor, status) VALUES (5, 'pending') RETURNING request_id;



-- ============= LOG QUERIES =============
-- Get all event logs
SELECT * FROM logs;

-- Get recent logs (last 10)
SELECT * FROM logs ORDER BY event_time DESC LIMIT 10;

-- Insert a new event log
INSERT INTO logs (lift_id, event_type) VALUES (1, 'door_open');

-- Get logs for a specific lift
SELECT * FROM logs WHERE lift_id = 1 ORDER BY event_time DESC;

INSERT INTO lifts (current_floor,direction,door_status)
VALUES
    (1,'idle','closed'),
    (3,'idle','closed'),
    (5,'idle','closed'),
    (7,'idle','closed');