#!/bin/bash

PGPASSWORD="" \
psql -h HOST -p PORT -U USERNAME \
-d coffee_canary -c "\copy staging.beans_raw (\
\"Purchase Date\",\"Roaster\",\"Blend Name\",\"Roast Level\",\"Roast Date\", \
\"Weight (g)\",\"Blend Type\",\"Notes\",\"Origin\",\"Variety\",\"Processing\", \
\"Bean Type\",\"URL\") \
FROM './data/coffee_beans.csv' WITH CSV HEADER"
