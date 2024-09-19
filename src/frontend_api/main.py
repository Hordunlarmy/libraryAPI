from decouple import config
from flask import Flask
from modules.book.blueprint import book_blueprint
from modules.user.blueprint import user_blueprint
from shared.logger import logging

app = Flask(__name__)


@app.route("/")
def read_root():
    return {"Hello": "This is the frontend API"}


app.register_blueprint(user_blueprint, url_prefix="/api/users")
app.register_blueprint(book_blueprint, url_prefix="/api/books")


consumer_started = False


@app.before_request
def start_consumer():
    """
    Start the RabbitMQ consumer thread once
    before the first request is processed.
    """

    import threading
    from shared.broker import SyncManager
    from shared.utils import callback

    global consumer_started
    if not consumer_started:
        consumer_thread = threading.Thread(
            target=SyncManager().consume, args=(callback,)
        )
        consumer_thread.start()
        consumer_started = True
        logging.info("RabbitMQ consumer started")
    else:
        logging.info("RabbitMQ consumer already running")


if __name__ == "__main__":

    debug = config("DEBUG", default=False, cast=bool)
    app.run(debug=debug, host="0.0.0.0", port=8001)
