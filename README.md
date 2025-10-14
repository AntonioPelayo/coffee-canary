# coffee-canary
Dashboard for monitoring coffee consumption metrics.

## Run (Local dev, no Docker)

1. Copy `.env.example` to `.env` and fill values.
2. Start the app:
   - Dev (auto reload): `build.sh -d`
   - Prod test (Gunicorn): `build.sh`
3. Access the app at `http://127.0.0.1:8050`

## Run (Docker)

1. Copy `.env.example` to `.env` and fill values (DB credentials, etc.).
2. Build image: `docker build -t coffee-canary .`
3. Run:
	- Direct: `docker run --env-file .env -p 8050:8050 coffee-canary`
	- Compose: `docker compose up --build`

Local app: http://0.0.0.0:8050

Data sources
- Postgres
- CSV fallback
