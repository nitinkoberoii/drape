# Docker

The root `docker-compose.yml` starts the Phase 0 local dependencies: PostgreSQL,
Redis, and Qdrant. Copy `.env.example` to `.env`, set a non-default database
password, then run `docker compose up -d`.
