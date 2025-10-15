# Coffee Canary DB

## Connections
Direct connection:
```bash
psql -h HOST -p PORT -U username -d coffee_canary
```

## Secrets
Stored in root directory .env

## Running SQL scripts on db
From project root:
```bash
psql "$DB_URL" -f db/setup/script.sql
```
With flags:
```bash
psql -h HOST -p PORT -U username -d coffee_canary -f db/setup/script.sql
```

### Setup script order
1. 001_create_schemas.sql
2. 002_dim_roaster.sql
3. 003_fact_coffee_beans.sql
4. 004_staging.sql
4.5 004_5_load_beans_csv.sql
4.5 004_5_load_roasters_csv.sql
5. 005_upsert_roasters.sql
6. 006_upsert_beans.sql
6. 006_upsert_roasters.sql