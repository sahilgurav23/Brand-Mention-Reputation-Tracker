CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS mentions (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50),
    url TEXT,
    author VARCHAR(100),
    content TEXT,
    sentiment VARCHAR(20),
    topic VARCHAR(50),
    embedding VECTOR(384),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
