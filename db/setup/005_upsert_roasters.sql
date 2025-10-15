-- Created on 2025-10-14
-- Take raw roasters from staging, normalize, then UPDATE existing / INSERT new into warehouse.dim_roaster

BEGIN;

-- Normalize incoming rows (trim/empty→NULL; case-insensitive match keys)
WITH roasters_clean AS (
  SELECT DISTINCT
    NULLIF(trim(src_name), '')  AS name,
    NULLIF(trim(city), '')      AS city,
    NULLIF(trim(state), '')     AS state,
    NULLIF(trim(country), '')   AS country,
    NULLIF(trim(website), '')   AS website,
    -- keys used for matching
    lower(NULLIF(trim(src_name), ''))  AS k_name,
    lower(COALESCE(NULLIF(trim(city), ''), ''))    AS k_city,
    lower(COALESCE(NULLIF(trim(state), ''), ''))   AS k_state,
    lower(COALESCE(NULLIF(trim(country), ''), '')) AS k_country
  FROM staging.roasters_raw
  WHERE NULLIF(trim(src_name), '') IS NOT NULL
),

-- Update existing rows (match on case-insensitive natural key)
updated AS (
  UPDATE warehouse.dim_roaster d
  SET
    city       = COALESCE(c.city, d.city),
    state      = COALESCE(c.state, d.state),
    country    = COALESCE(c.country, d.country),
    website    = COALESCE(c.website, d.website)
  FROM roasters_clean c
  WHERE lower(d.name)   = c.k_name
    AND lower(COALESCE(d.city, ''))    = c.k_city
    AND lower(COALESCE(d.state, ''))   = c.k_state
    AND lower(COALESCE(d.country, '')) = c.k_country
  RETURNING d.roaster_id
)

-- Insert only those that didn’t match an existing row
INSERT INTO warehouse.dim_roaster (name, city, state, country, website)
SELECT c.name, c.city, c.state, c.country, c.website
FROM roasters_clean c
LEFT JOIN warehouse.dim_roaster d
  ON lower(d.name)   = c.k_name
 AND lower(COALESCE(d.city, ''))    = c.k_city
 AND lower(COALESCE(d.state, ''))   = c.k_state
 AND lower(COALESCE(d.country, '')) = c.k_country
WHERE d.roaster_id IS NULL;

COMMIT;

-- Check (run separately, optional)
-- SELECT COUNT(*) FROM warehouse.dim_roaster;