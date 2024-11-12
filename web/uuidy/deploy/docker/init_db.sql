CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY ,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    tg_chat_id BIGINT DEFAULT NULL,
    is_admin bool DEFAULT false
);

CREATE TABLE notes (
    user_id BIGINT,
    note_id BIGSERIAL,
    content TEXT,
    PRIMARY KEY (user_id, note_id)
);

CREATE USER ro_user WITH PASSWORD 'ro_user';
GRANT CONNECT ON DATABASE postgres TO ro_user;
GRANT USAGE ON SCHEMA public TO ro_user;
GRANT SELECT ON TABLE Users, Notes TO ro_user;
ALTER DEFAULT PRIVILEGES FOR ROLE ro_user IN SCHEMA public REVOKE ALL ON TABLES FROM ro_user;
