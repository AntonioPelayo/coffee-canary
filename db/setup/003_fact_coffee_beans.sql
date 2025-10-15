-- Created on 2025-10-14
-- Fact table for individual bean purchases/bags, linked to dim_roaster

BEGIN;

CREATE TABLE IF NOT EXISTS warehouse.fact_coffee_beans (
  bean_id       UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  roaster_id    UUID NOT NULL, -- FK to dim_roaster

  -- core fields (nullable to tolerate sparse CSVs)
  purchase_date DATE,
  roast_date    DATE,
  blend_name    TEXT,
  roast_level   TEXT,
  weight_g      NUMERIC(10,2),
  blend_type    TEXT,
  notes         TEXT,
  origin        TEXT,
  variety       TEXT,
  processing    TEXT,
  bean_type     TEXT,
  url           TEXT,

  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Foreign key to roasters dimension
  CONSTRAINT fk_fact_beans_roaster
    FOREIGN KEY (roaster_id) REFERENCES warehouse.dim_roaster(roaster_id)
      ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Uniqueness to prevent duplicate loads
CREATE UNIQUE INDEX IF NOT EXISTS uq_fact_beans_dedupe
ON warehouse.fact_coffee_beans (
  roaster_id,
  COALESCE(lower(blend_name), ''),
  purchase_date,
  COALESCE(weight_g, 0)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_fact_beans_roaster ON warehouse.fact_coffee_beans (roaster_id);
CREATE INDEX IF NOT EXISTS idx_fact_beans_purchase_date ON warehouse.fact_coffee_beans (purchase_date);
CREATE INDEX IF NOT EXISTS idx_fact_beans_roast_level ON warehouse.fact_coffee_beans (lower(roast_level));

-- updated_at trigger
CREATE OR REPLACE FUNCTION warehouse.tg_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at := NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trig_fact_beans_set_updated_at ON warehouse.fact_coffee_beans;
CREATE TRIGGER trig_fact_beans_set_updated_at
BEFORE UPDATE ON warehouse.fact_coffee_beans
FOR EACH ROW EXECUTE FUNCTION warehouse.tg_set_updated_at();

COMMIT;