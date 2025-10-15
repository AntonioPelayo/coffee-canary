-- Created on 2025-10-14
-- Raw landing tables for CSV loads (no FKs, wide TEXT columns)

BEGIN;

CREATE TABLE IF NOT EXISTS staging.roasters_raw (
  src_name   TEXT,   -- "name" from CSV
  city       TEXT,
  state      TEXT,
  country    TEXT,
  website    TEXT,
  _ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS staging.beans_raw (
  "Purchase Date"   TEXT,
  "Roaster"         TEXT,
  "Blend Name"      TEXT,
  "Roast Level"     TEXT,
  "Roast Date"      TEXT,
  "Weight (g)"      TEXT,
  "Blend Type"      TEXT,
  "Notes"           TEXT,
  "Origin"          TEXT,
  "Variety"         TEXT,
  "Processing"      TEXT,
  "Bean Type"       TEXT,
  "URL"             TEXT,
  _ingested_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_roasters_raw_ingested_at ON staging.roasters_raw (_ingested_at);
CREATE INDEX IF NOT EXISTS idx_beans_raw_ingested_at    ON staging.beans_raw(_ingested_at);

COMMIT;