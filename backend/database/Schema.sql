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
    status VARCHAR(10) CHECK (status IN ('pending','served')),
    lift_id INT,
    CONSTRAINT fk_req_lift
        FOREIGN KEY (lift_id)
        REFERENCES lifts(lift_id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS logs (
    log_id SERIAL PRIMARY KEY,
    lift_id INT,
    event_type VARCHAR(50),
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_lift
        FOREIGN KEY (lift_id)
        REFERENCES lifts(lift_id)
        ON DELETE CASCADE
);
