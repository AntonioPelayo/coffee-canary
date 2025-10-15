#!/bin/bash

PGPASSWORD="" \
psql -h HOST -p PORT -U USERNAME \
-d coffee_canary -c "\copy staging.roasters_raw (src_name, city, state) \
FROM './data/coffee_roasters.csv' WITH CSV HEADER"
