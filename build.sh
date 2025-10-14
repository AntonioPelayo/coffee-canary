#!/bin/bash

set -e

# Dev flag
DEV=false
if [ "${1:-}" = "-d" ]; then
    DEV=true
fi

# Load .env
if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi

# Python/Gunicorn venv
PY=python
GUNICORN=gunicorn
if [ -x ./venv/bin/python ]; then PY=./venv/bin/python; fi
if [ -x ./venv/bin/gunicorn ]; then GUNICORN=./venv/bin/gunicorn; fi


# Dev vs prod
if $DEV; then
  echo "→ DEV mode (DEBUG=True)"
  DEBUG=True exec "$PY" -m src.app
else
  echo "→ PROD mode (gunicorn)"
  : "${DEBUG:=False}"   # default DEBUG to False if not set in .env
  exec "$GUNICORN" -b "${HOST:-127.0.0.1}:${PORT:-8050}" src.app:server
fi
