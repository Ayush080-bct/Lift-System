-- Lifts table
CREATE TABLE IF NOT EXISTS lifts (
    lift_id SERIAL PRIMARY KEY,
    current_floor INT NOT NULL DEFAULT 0, -- start at the ground floor
    direction VARCHAR(10) DEFAULT 'idle' CHECK (direction IN ('up','down','idle')),
    door_status VARCHAR(10) DEFAULT 'closed' CHECK (door_status IN ('open','closed'))
);

-- Requests table
CREATE TABLE IF NOT EXISTS requests (
    request_id SERIAL PRIMARY KEY,
    floor INT NOT NULL CHECK (floor >= 0),  -- ✅ No negative floors
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(10) DEFAULT 'pending' CHECK (status IN ('pending','served')),
    lift_id INT,
    CONSTRAINT fk_req_lift
        FOREIGN KEY (lift_id)
        REFERENCES lifts(lift_id)
        ON DELETE CASCADE  -- ✅ Clean up orphaned requests
);

-- Logs table
CREATE TABLE IF NOT EXISTS logs (
    log_id SERIAL PRIMARY KEY,
    lift_id INT NOT NULL,  -- ✅ Every log belongs to a lift
    event_type VARCHAR(50) CHECK (event_type IN (
        'button_pressed', 'lift_arrived', 'door_opened', 'door_closed', 'emergency_stop'
    )),
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_lift
        FOREIGN KEY (lift_id)
        REFERENCES lifts(lift_id)
        ON DELETE CASCADE
);

-- Seed data: Insert default lifts
INSERT INTO lifts (lift_id, current_floor, direction, door_status)
VALUES 
    (1, 0, 'idle', 'closed'),
    (2, 0, 'idle', 'closed')
ON CONFLICT (lift_id) DO NOTHING;

-- cascade is the referential action used with foreign kkey to automatically propagate changes from the parent table down to related child tables.
-- it maintains referential integrity by ensuring  that when the data in the primary column is modified 
-- or remoooved , all dependent data in secondary tables updates or deletes.

-- on delete cascade : when you delete a row from the parent table ,sql automaticallly deletes all corresponding row in the child table