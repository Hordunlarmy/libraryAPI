from datetime import datetime, timedelta

from bson import ObjectId
from flask import jsonify
from shared.broker import SyncManager
from shared.database import db as frontend_db
from shared.logger import logging

broker = SyncManager()


class BookManager:
    """
    Class to handle book operations
    """

    def __init__(self, db=frontend_db):
        """
        Class initialization with the database
        """

        self.db = db

    def list_all_available_books(self):
        """
        Method to list all available books
        """

        available_books = self.db.Books.find({"is_borrowed": False})
        books_list = list(available_books)

        for book in books_list:
            book["_id"] = str(book["_id"])

        return jsonify(books_list), 200

    def get_book_by_id(self, book_id):
        """
        Method to get a book by its ID
        """

        book_id = ObjectId(book_id)
        book = self.db.Books.find_one({"_id": book_id})

        if not book:
            logging.error("Book not found")
            return jsonify({"error": "Book not found"}), 404

        book["_id"] = str(book["_id"])

        return jsonify(book), 200

    def borrow_book(self, borrow_data):
        """
        Method to borrow a book for a specified number of days.
        """

        borrow_data = borrow_data.dict()

        user_id = borrow_data.get("user_id")
        book_id = borrow_data.get("book_id")
        due_days = borrow_data.get("days")

        due_date = datetime.utcnow() + timedelta(days=due_days)

        self.db.Books.update_one(
            {"_id": book_id}, {"$set": {"is_borrowed": True}}
        )

        self.db.BorrowedBooks.insert_one(
            {
                "user_id": user_id,
                "book_id": book_id,
                "borrow_date": datetime.utcnow(),
                "return_date": due_date,
            }
        )

        return jsonify({"message": "Book borrowed successfully"}), 200

    def return_book(self, data):
        """
        Method to return a borrowed book
        """

        book_id = data.dict().get("book_id")

        self.db.Books.update_one(
            {"_id": book_id}, {"$set": {"is_borrowed": False}}
        )

        self.db.BorrowedBooks.delete_one({"book_id": book_id})

        return jsonify({"message": "Book returned successfully"}), 200

    def filter_books(self, publishers=None, categories=None):
        """
        Filter books by publishers and categories.
        """

        query = {}

        # Filter out empty strings from publishers and categories
        publishers = [p for p in publishers if p] if publishers else []
        categories = [c for c in categories if c] if categories else []

        logging.info(f"{publishers=} {categories=}")

        if publishers:
            query["publisher"] = {"$in": publishers}

        if categories:
            query["category"] = {"$in": categories}

        books = self.db.Books.find(query)
        books_list = list(books)

        for book in books_list:
            book["_id"] = str(book["_id"])

        return jsonify(books_list), 200
