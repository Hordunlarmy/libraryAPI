import json
import uuid

from shared.logger import logging


def callback(ch, method, properties, body):
    """
    Callback function to handle incoming messages from the RabbitMQ broker.
    """

    from modules.book.manager import BookManager

    body = json.loads(body.decode("utf-8"))
    response = BookManager().sync_book(body)

    logging.info(response)


def generate_uuid():
    """
    Generate a unique identifier.
    """

    return str(uuid.uuid4())
