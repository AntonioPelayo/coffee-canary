-- Created on 2025-10-14
-- Purpose: Define dimension table for coffee_roasters in the warehouse schema.
-- Dimensions: one row per roaster

BEGIN;

CREATE TABLE IF NOT EXISTS warehouse.dim_roaster (
  roaster_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name       TEXT NOT NULL,
  city       TEXT,
  state      TEXT,
  country    TEXT,
  website    TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Prevent dupes: same name + (city,state,country) once, case-insensitive
CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_roaster_natkey
ON warehouse.dim_roaster (
    lower(name),
    COALESCE(lower(city), ''),
    COALESCE(lower(state), ''),
    COALESCE(lower(country), '')
);

-- Upsert name matching
CREATE INDEX IF NOT EXISTS idx_dim_roaster_name
ON warehouse.dim_roaster (lower(name));

-- Auto-update updated_at on any UPDATE
CREATE OR REPLACE FUNCTION warehouse.tg_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trig_dim_roaster_set_updated_at ON warehouse.dim_roaster;
CREATE TRIGGER trig_dim_roaster_set_updated_at
BEFORE UPDATE ON warehouse.dim_roaster
FOR EACH ROW EXECUTE FUNCTION warehouse.tg_set_updated_at();

COMMIT;
