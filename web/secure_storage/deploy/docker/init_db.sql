CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY ,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_paid bool DEFAULT false
);