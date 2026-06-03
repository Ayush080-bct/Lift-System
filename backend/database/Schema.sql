-- Lifts table
CREATE TABLE IF NOT EXISTS lifts (
    lift_id SERIAL PRIMARY KEY,
    current_floor INT NOT NULL DEFAULT 1 CHECK (current_floor >= 1 AND current_floor <= 10),
    direction VARCHAR(10) DEFAULT 'idle' CHECK (direction IN ('up','down','idle')),
    door_status VARCHAR(10) DEFAULT 'closed' CHECK (door_status IN ('open','closed'))
);

-- Requests table
CREATE TABLE IF NOT EXISTS requests (
    request_id SERIAL PRIMARY KEY,
    floor INT NOT NULL CHECK (floor >= 1 AND floor <= 10),
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(10) DEFAULT 'pending' CHECK (status IN ('pending','served')),
    lift_id INT,
    CONSTRAINT fk_req_lift
        FOREIGN KEY (lift_id)
        REFERENCES lifts(lift_id)
        ON DELETE CASCADE
);

-- Logs table (enum values enforced in app)
CREATE TABLE IF NOT EXISTS logs (
    log_id SERIAL PRIMARY KEY,
    lift_id INT NOT NULL,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN (
        'button_pressed', 'lift_arrived', 'door_opened', 'door_closed', 'emergency_stop'
    )),
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_lift
        FOREIGN KEY (lift_id)
        REFERENCES lifts(lift_id)
        ON DELETE CASCADE
);

-- Single lift for phase 1 (add more rows when scaling)
INSERT INTO lifts (lift_id, current_floor, direction, door_status)
VALUES (1, 1, 'idle', 'closed')
ON CONFLICT (lift_id) DO NOTHING;
