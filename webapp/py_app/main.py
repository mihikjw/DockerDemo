import connexion
import os
import sys
import logging
from flask_cors import CORS
from api.initialization import init_http_handlers


def quit_error(msg: str):
    "exit the app with an error"
    logging.error(msg)
    sys.exit(1)


app = connexion.FlaskApp(__name__, specification_dir=".")
app.add_api("api_schema.yml")
CORS(app.app)

try:
    init_http_handlers(os.getenv("REDIS_HOST", "localhost"), int(os.getenv("REDIS_PORT", 6379)), os.getenv("REDIS_PASS", ""))
except ValueError as ex:
    quit_error(f"Missing Config Values: {str(ex)}")
except ConnectionError as ex:
    quit_error(f"Error Connecting To Redis: {str(ex)}")

if __name__ == "__main__":
    app.run(port=6006)
