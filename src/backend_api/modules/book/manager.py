import json
from datetime import datetime

from decouple import config
from fastapi import HTTPException
from modules.book.schemas import BookCreateSchema, UnavailableBook
from shared.broker import SyncManager
from shared.database import Database, db
from shared.logger import logging
from shared.utils import generate_uuid

broker = SyncManager()


class BookManager:
    def __init__(
        self,
        database: Database = db,
        pub_queue: str = config("BROKER_PUB_QUEUE"),
    ):
        self.db = database
        self.pub_queue = pub_queue

    async def add_book(self, book_data: BookCreateSchema):
        """
        Add a new book to the database
        """

        query = """
        INSERT INTO Books (id, title, author, category, publisher)
        VALUES (%s, %s, %s, %s, %s)
        """

        book_id = generate_uuid()

        params = (
            book_id,
            book_data.title,
            book_data.author,
            book_data.category,
            book_data.publisher,
        )

        try:
            self.db.commit(query, params)
        except Exception as e:
            logging.error(f"Error adding book: {e}")
            return HTTPException(status_code=500, detail="Error adding book")

        try:
            book_data_dict = book_data.dict()
            book_data_dict["_id"] = book_id
            book_data_dict["action"] = "add_book"
            message = json.dumps(book_data_dict).encode("utf-8")
            broker.publish(message, self.pub_queue)
        except Exception as e:
            logging.error(f"Error publishing book data: {e}")
            try:
                rollback_query = """
                DELETE FROM Books
                WHERE id = %s
                """
                rollback_params = (book_id,)
                self.db.commit(rollback_query, rollback_params)
                logging.info("Rolled back book insertion successfully.")
                raise HTTPException(
                    status_code=500,
                    detail="Broker connection error. Try again",
                )
            except Exception as rollback_error:
                logging.error(f"Error during rollback: {rollback_error}")
                raise HTTPException(status_code=500, detail="Rollback failed")

            raise HTTPException(status_code=500, detail="Rollback performed")

        return {"book_id": book_id}

    async def remove_book(self, book_id: int):
        """
        Remove a book from the database
        """

        query = """
        DELETE FROM Books
        WHERE id = %s
        """

        params = (book_id,)

        try:
            self.db.commit(query, params)
        except Exception as e:
            logging.error(f"Error removing book: {e}")
            raise HTTPException(status_code=500, detail="Error removing book")

        try:
            book_data = {"book_id": book_id, "action": "remove_book"}
            book_data = json.dumps(book_data).encode("utf-8")
            broker.publish(book_data, self.pub_queue)
        except Exception as e:
            logging.error(f"Error publishing book data: {e}")

            try:
                rollback_query = """
                INSERT INTO Books (id)
                VALUES (%s)
                """
                rollback_params = (book_id,)
                self.db.commit(rollback_query, rollback_params)
                logging.info("Rolled back book removal successfully.")
                raise HTTPException(
                    status_code=500,
                    detail="Broker connection error. Try again",
                )
            except Exception as rollback_error:
                logging.error(f"Error during rollback: {rollback_error}")
                raise HTTPException(status_code=500, detail="Rollback failed")

            raise HTTPException(status_code=500, detail="Rollback performed")

        return {"message": "Book removed successfully"}

    def sync_borrowed_book(self, book_data):
        """
        Sync borrowed book data asynchronously.
        """

        borrowed_query = """
        INSERT INTO 
        BorrowedBooks (id, user_id, book_id, borrow_date, return_date)
        VALUES (%s, %s, %s, %s, %s)
        """

        book_query = """
            UPDATE Books
            SET is_borrowed = true
            WHERE id = %s
            """

        params = (
            book_data.get("_id"),
            book_data.get("user_id"),
            book_data.get("book_id"),
            datetime.fromisoformat(book_data.get("borrow_date")),
            datetime.fromisoformat(book_data.get("return_date")),
        )

        try:
            self.db.commit(borrowed_query, params)
            self.db.commit(book_query, (book_data.get("book_id"),))

            return {"message": "Borrowed book synced successfully"}
        except Exception as e:
            logging.error(f"Error syncing borrowed book: {e}")
            return {"error": f"Error syncing borrowed book: {str(e)}"}, 500

    def sync_returned_book(self, book_data):
        """
        Sync returned book data asynchronously.
        """

        book_query = """
            UPDATE Books
            SET is_borrowed = false
            WHERE id = %s
            """

        borrowed_query = """
        DELETE FROM BorrowedBooks
        WHERE book_id = %s
        """

        try:
            self.db.commit(book_query, (book_data.get("book_id"),))
            self.db.commit(borrowed_query, (book_data.get("book_id"),))

            return {"message": "Returned book synced successfully"}
        except Exception as e:
            logging.error(f"Error syncing returned book: {e}")
            return {"error": f"Error syncing returned book: {str(e)}"}, 500

    async def get_unavailable_books(self) -> list[UnavailableBook]:
        """
        Get all unavailable books.
        """

        query = """
        SELECT 
            Books.id AS book_id, 
            Books.title, 
            Books.author, 
            Books.publisher, 
            Books.category, 
            BorrowedBooks.return_date AS available_on
        FROM 
            Books
        JOIN 
            BorrowedBooks ON Books.id = BorrowedBooks.book_id
        WHERE 
            BorrowedBooks.return_date > CURRENT_DATE;
        """

        books_data = self.db.select(query)

        unavailable_books = [
            UnavailableBook(
                id=record["book_id"],
                title=record["title"],
                author=record["author"],
                publisher=record["publisher"],
                category=record["category"],
                available_on=record["available_on"],
            )
            for record in books_data
        ]

        return unavailable_books
