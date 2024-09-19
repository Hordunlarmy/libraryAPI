from shared.logger import logging
import uuid
import json


def callback(ch, method, properties, body):
    """
    Callback function to handle incoming messages from the RabbitMQ broker.
    """

    from modules.user.manager import UserManager
    from modules.book.manager import BookManager

    body = json.loads(body.decode("utf-8"))

    if body["action"] == "enroll_user":
        response = UserManager().sync_user(body)

    if body["action"] == "borrow_book":
        response = BookManager().sync_borrowed_book(body)

    if body["action"] == "return_book":
        response = BookManager().sync_returned_book(body)

    logging.info(response)


def generate_uuid():
    """
    Generate a unique identifier.
    """

    return str(uuid.uuid4())
