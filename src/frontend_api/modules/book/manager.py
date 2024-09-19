import json
from datetime import datetime, timedelta

from decouple import config
from flask import jsonify
from shared.broker import SyncManager
from shared.database import db as frontend_db
from shared.logger import logging
from shared.utils import generate_uuid

broker = SyncManager()


class BookManager:
    """
    Class to handle book operations
    """

    def __init__(self, db=frontend_db, pub_queue=config("BROKER_PUB_QUEUE")):
        """
        Class initialization with the database
        """

        self.db = db
        self.pub_queue = pub_queue

    def sync_book(self, book_data):
        """
        Method to sync book data with the backend API
        """
        from main import app

        with app.app_context():

            if book_data.get("action") == "add_book":
                book_data.pop("action")
                book_data["created_at"] = datetime.utcnow()
                book_data["is_borrowed"] = False

                try:
                    self.db.Books.insert_one(book_data)
                except Exception as e:
                    logging.error(f"Error syncing book(add): {e}")
                    return jsonify({"error": "Error syncing book(add)"}), 500

                return jsonify({"message": "Book synced successfully"}), 200
            elif book_data.get("action") == "remove_book":
                book_id = book_data.get("book_id")

                try:
                    self.db.Books.delete_one({"_id": book_id})
                except Exception as e:
                    logging.error(f"Error syncing book(remove): {e}")
                    return (
                        jsonify({"error": "Error syncing book(remove)"}),
                        500,
                    )

                return jsonify({"message": "Book removed successfully"}), 200

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
        borrow_data["_id"] = generate_uuid()
        borrow_data["borrow_date"] = datetime.utcnow()
        borrow_data["return_date"] = datetime.utcnow() + timedelta(
            days=int(borrow_data.get("days"))
        )
        borrow_data.pop("days")

        try:
            self.db.Books.update_one(
                {"_id": borrow_data.get("book_id")},
                {"$set": {"is_borrowed": True}},
            )

            self.db.BorrowedBooks.insert_one(borrow_data)
        except Exception as e:
            logging.error(f"Error borrowing book: {e}")
            return jsonify({"error": "Error borrowing book"}), 500

        try:
            borrow_data["action"] = "borrow_book"
            borrow_data["borrow_date"] = borrow_data["borrow_date"].isoformat()
            borrow_data["return_date"] = borrow_data["return_date"].isoformat()
            borrow_data_json = json.dumps(borrow_data)
            broker.publish(borrow_data_json, self.pub_queue)
        except Exception as e:
            logging.error(f"Error borrowing book: {e}")
            return jsonify({"error": "Error borrowing book"}), 500

        return jsonify({"message": "Book borrowed successfully"}), 200

    def return_book(self, data):
        """
        Method to return a borrowed book
        """

        book_id = data.dict().get("book_id")

        try:
            self.db.Books.update_one(
                {"_id": book_id}, {"$set": {"is_borrowed": False}}
            )

            self.db.BorrowedBooks.delete_one({"book_id": book_id})
        except Exception as e:
            logging.error(f"Error returning book: {e}")
            return jsonify({"error": "Error returning book"}), 500

        try:
            return_data = {"book_id": book_id, "action": "return_book"}
            return_data_json = json.dumps(return_data)
            broker.publish(return_data_json, self.pub_queue)
        except Exception as e:
            logging.error(f"Error returning book: {e}")
            return jsonify({"error": "Error returning book"}), 500

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
