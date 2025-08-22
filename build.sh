# Load environment variables from .env
export $(grep -v '^#' .env | xargs)

# Local web app
## Development with auto reload
./venv/bin/python -m pip install -r requirements.txt
# ./venv/bin/python -m src.app.app

# Gunicorn server
./venv/bin/gunicorn src.app.app:server -w 2 -b 0.0.0.0:8050

# Unset the environment variables
unset $(grep -v '^#' .env | sed -E 's/(.*)=.*/\1/' | xargs)