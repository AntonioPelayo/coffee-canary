# coffee-canary
Morning alerts and data visualizations to optimize your daily brew

## Run (Docker)

1. Copy `.env.example` to `.env` and fill values (DB credentials, etc.).
2. Build image: `docker build -t coffee-canary .`
3. Run:
	- Direct: `docker run --env-file .env -p 8050:8050 coffee-canary`
	- Compose: `docker compose up --build`

App: http://0.0.0.0:8050

Data sources
- Postgres
- CSV fallback
