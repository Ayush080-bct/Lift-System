CREATE TABLE IF NOT EXISTS lifts (
    lift_id SERIAL PRIMARY KEY,
    current_floor INT NOT NULL,
    direction VARCHAR(10) CHECK (direction IN ('up','down','idle')),
    door_status VARCHAR(10) CHECK (door_status IN ('open','closed'))
);

CREATE TABLE IF NOT EXISTS requests (
    request_id SERIAL PRIMARY KEY,
    floor INT NOT NULL,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(10) DEFAULT 'pending',
    lift_id INT,
    CONSTRAINT fk_req_lift
        FOREIGN KEY (lift_id)
        REFERENCES lifts(lift_id)
        ON DELETE SET NULL  -- If a lift is deleted, set lift_id to NULL (keep the request record)
);

CREATE TABLE IF NOT EXISTS logs (
    log_id SERIAL PRIMARY KEY,
    lift_id INT,
    event_type VARCHAR(50),
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_lift
        FOREIGN KEY (lift_id)
        REFERENCES lifts(lift_id)
        ON DELETE CASCADE  -- If a lift is deleted, automatically delete all its log records
);
ALTER TABLE logs 
ADD CONSTRAINT chk_event_type CHECK (event_type IN ('button_pressed','lift_arrived','door_opened','door_closed','emergency_stop'))

DROP TABLE requests CASCADE;