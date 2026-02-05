# Coffee Canary
Dashboard for monitoring coffee purchase metrics and trends.

## Run (Local dev, no Docker)
1. Copy `.env.example` to `.env` and fill values.
2. Start the app:
   - Dev (auto reload): `bin/build_local.sh -d`
   - Prod test (Gunicorn): `bin/build_local.sh`
3. Access the app at `http://127.0.0.1:8050`

## Data sources
- coffee_canary.db (SQLite)
- CSV fallback
