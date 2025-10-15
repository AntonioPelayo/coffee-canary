-- Created on 2025-10-14
-- Load staging.beans_raw -> warehouse.fact_coffee_beans (idempotent)

BEGIN;

WITH beans_clean AS (
  SELECT
    NULLIF(trim("Roaster"), '')           AS roaster_name,
    NULLIF(trim("Blend Name"), '')        AS blend_name,
    NULLIF(trim("Roast Level"), '')       AS roast_level,
    NULLIF(trim("Blend Type"), '')        AS blend_type,
    NULLIF(trim("Notes"), '')             AS notes,
    NULLIF(trim("Origin"), '')            AS origin,
    NULLIF(trim("Variety"), '')           AS variety,
    NULLIF(trim("Processing"), '')        AS processing,
    NULLIF(trim("Bean Type"), '')         AS bean_type,
    NULLIF(trim("URL"), '')               AS url,

    -- Date parsing: ISO first, then mm/dd/yyyy
    CASE
      WHEN "Purchase Date" ~ '^\d{4}-\d{2}-\d{2}$'    THEN to_date("Purchase Date", 'YYYY-MM-DD')
      WHEN "Purchase Date" ~ '^\d{1,2}/\d{1,2}/\d{4}$' THEN to_date("Purchase Date", 'MM/DD/YYYY')
      ELSE NULL
    END AS purchase_date,
    CASE
      WHEN "Roast Date" ~ '^\d{4}-\d{2}-\d{2}$'    THEN to_date("Roast Date", 'YYYY-MM-DD')
      WHEN "Roast Date" ~ '^\d{1,2}/\d{1,2}/\d{4}$' THEN to_date("Roast Date", 'MM/DD/YYYY')
      ELSE NULL
    END AS roast_date,

    -- bean weight: strip non-numeric, cast to numeric
    NULLIF(regexp_replace("Weight (g)", '[^0-9\.]', '', 'g'), '')::numeric AS weight_g
  FROM staging.beans_raw
),

-- Ensure all roasters referenced by beans exist in dim_roaster
new_roasters AS (
  INSERT INTO warehouse.dim_roaster (name)
  SELECT DISTINCT bc.roaster_name
  FROM beans_clean bc
  LEFT JOIN warehouse.dim_roaster d
    ON lower(d.name) = lower(bc.roaster_name)
  WHERE bc.roaster_name IS NOT NULL
    AND d.roaster_id IS NULL
  RETURNING roaster_id, name
),

-- Map beans to roaster_id
beans_mapped AS (
  SELECT
    COALESCE(d.roaster_id, nr.roaster_id) AS roaster_id,
    bc.blend_name,
    bc.roast_level,
    bc.blend_type,
    bc.notes,
    bc.origin,
    bc.variety,
    bc.processing,
    bc.bean_type,
    bc.url,
    bc.purchase_date,
    bc.roast_date,
    bc.weight_g
  FROM beans_clean bc
  LEFT JOIN warehouse.dim_roaster d
    ON lower(d.name) = lower(bc.roaster_name)
  LEFT JOIN new_roasters nr
    ON lower(nr.name) = lower(bc.roaster_name)
  WHERE bc.roaster_name IS NOT NULL
),

-- Update existing facts, dedupe logic
updated AS (
  UPDATE warehouse.fact_coffee_beans f
  SET
    roast_level = COALESCE(bm.roast_level, f.roast_level),
    blend_type  = COALESCE(bm.blend_type,  f.blend_type),
    notes       = COALESCE(bm.notes,       f.notes),
    origin      = COALESCE(bm.origin,      f.origin),
    variety     = COALESCE(bm.variety,     f.variety),
    processing  = COALESCE(bm.processing,  f.processing),
    bean_type   = COALESCE(bm.bean_type,   f.bean_type),
    url         = COALESCE(bm.url,         f.url),
    roast_date  = COALESCE(bm.roast_date,  f.roast_date),
    weight_g    = COALESCE(bm.weight_g,    f.weight_g)
  FROM beans_mapped bm
  WHERE f.roaster_id = bm.roaster_id
    AND lower(COALESCE(f.blend_name, '')) = lower(COALESCE(bm.blend_name, ''))
    AND f.purchase_date IS NOT DISTINCT FROM bm.purchase_date
    AND COALESCE(f.weight_g, 0) = COALESCE(bm.weight_g, 0)
  RETURNING f.bean_id
)

-- Insert new facts that didn't match existing rows
INSERT INTO warehouse.fact_coffee_beans (
  roaster_id, blend_name, roast_level, blend_type, notes,
  origin, variety, processing, bean_type, url,
  purchase_date, roast_date, weight_g
)
SELECT
  bm.roaster_id, bm.blend_name, bm.roast_level, bm.blend_type, bm.notes,
  bm.origin, bm.variety, bm.processing, bm.bean_type, bm.url,
  bm.purchase_date, bm.roast_date, bm.weight_g
FROM beans_mapped bm
LEFT JOIN warehouse.fact_coffee_beans f
  ON f.roaster_id = bm.roaster_id
 AND lower(COALESCE(f.blend_name, '')) = lower(COALESCE(bm.blend_name, ''))
 AND f.purchase_date IS NOT DISTINCT FROM bm.purchase_date
 AND COALESCE(f.weight_g, 0) = COALESCE(bm.weight_g, 0)
WHERE f.bean_id IS NULL;

COMMIT;