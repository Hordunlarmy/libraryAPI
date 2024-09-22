import threading

from decouple import config
from flask import Flask, jsonify
from modules.book.blueprint import book_blueprint
from modules.user.blueprint import user_blueprint
from pydantic import ValidationError
from shared.broker import SyncManager
from shared.error_handler import CustomError
from shared.logger import logging

app = Flask(__name__)


@app.errorhandler(CustomError)
def handle_custom_error(error):
    response = jsonify({"error": error.message})
    response.status_code = error.http_status_code
    return response


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """
    Handle validation errors
    """

    first_error = error.errors()[0]
    error_msg = first_error.get("msg")
    error_loc = first_error.get("loc")

    response = jsonify(
        {
            "error": f"{error_msg} : {error_loc}",
        }
    )
    response.status_code = 400  # Bad Request
    return response


@app.route("/")
def read_root():
    return {"Hello": "This is the frontend API"}


app.register_blueprint(user_blueprint, url_prefix="/api/users")
app.register_blueprint(book_blueprint, url_prefix="/api/books")


consumer_started = False
sync_manager = SyncManager()


@app.before_request
def start_consumer():
    """
    Start the RabbitMQ consumer thread once
    before the first request is processed.
    """

    from shared.utils import callback

    global consumer_started

    if not consumer_started or not sync_manager.is_connected():
        if not sync_manager.is_connected():
            logging.warning("RabbitMQ connection lost, reconnecting...")
            sync_manager.reconnect()

        consumer_thread = threading.Thread(
            target=sync_manager.consume, args=(callback,)
        )
        consumer_thread.start()
        consumer_started = True
        logging.info("RabbitMQ consumer started")
    else:
        logging.info("RabbitMQ consumer already running")


if __name__ == "__main__":

    debug = config("DEBUG", default=False, cast=bool)
    app.run(debug=debug, host="0.0.0.0", port=8001)
