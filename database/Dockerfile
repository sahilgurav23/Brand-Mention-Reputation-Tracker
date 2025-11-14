FROM postgres:16

# Install pgvector extension
RUN apt-get update && apt-get install -y \
    postgresql-16-pgvector \
 && rm -rf /var/lib/apt/lists/*

# Copy initialization scripts (schema, extensions)
COPY init /docker-entrypoint-initdb.d/
