# Load environment variables from .env
export $(grep -v '^#' .env | xargs)

# Local web app
## Development with auto reload
./venv/bin/python -m pip install -r requirements.txt
# ./venv/bin/python -m src.app

# Gunicorn server
./venv/bin/gunicorn src.app:server

# Unset the environment variables
unset $(grep -v '^#' .env | sed -E 's/(.*)=.*/\1/' | xargs)