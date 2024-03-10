CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,

    url VARCHAR(256) NOT NULL,
    title VARCHAR(256),
    vendor VARCHAR(256),

    user_telegram_id VARCHAR(128) NOT NULL,

    UNIQUE(url, user_telegram_id)
);

CREATE USER testuser WITH PASSWORD 'testpassword';
GRANT ALL PRIVILEGES ON DATABASE "database" to testuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO testuser;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO testuser;
