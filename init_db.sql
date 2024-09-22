DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_database
        WHERE datname = 'shathishwarmas'
    ) THEN
        CREATE DATABASE shathishwarmas;
    END IF;
END $$;

\connect shathishwarmas;

CREATE TABLE IF NOT EXISTS lookup_logs (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    ipv4_addresses VARCHAR(255),
    ip_address VARCHAR(50),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    client_ip VARCHAR(50)
);
