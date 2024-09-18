from flask import Blueprint, request
from modules.book.manager import BookManager
from shared.logger import logging  # noqa
from shared.error_handler import error_handler
from modules.book.schemas import BorrowedBookSchema, ReturnedBookSchema

book_manager = BookManager()
book_blueprint = Blueprint("book", __name__)


@book_blueprint.route("/available", strict_slashes=False)
@error_handler()
def available():
    """
    Get all available books
    """

    return book_manager.list_all_available_books()


@book_blueprint.route("/<book_id>", strict_slashes=False)
def get_book(book_id):
    """
    Get a book by id
    """

    return book_manager.get_book_by_id(book_id)


@book_blueprint.route("/borrow", methods=["POST"], strict_slashes=False)
@error_handler(BorrowedBookSchema)
def borrow_book(borrow_data):
    """
    Borrow a book
    """

    return book_manager.borrow_book(borrow_data)


@book_blueprint.route("/return", methods=["POST"], strict_slashes=False)
@error_handler(ReturnedBookSchema)
def return_book(data):
    """
    Return a book
    """

    return book_manager.return_book(data)


@book_blueprint.route("/filter", methods=["POST"], strict_slashes=False)
def filter_books():
    """
    Filter books by publishers and categories.
    """

    publishers = request.args.getlist("publishers")
    categories = request.args.getlist("categories")

    return book_manager.filter_books(
        publishers=publishers, categories=categories
    )
