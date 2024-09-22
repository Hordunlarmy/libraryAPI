from pydantic import BaseModel, validator
from shared.database import db as frontend_db
from shared.error_handler import CustomError
from shared.logger import logging


class BorrowedBookSchema(BaseModel):
    """
    Pydantic schema for borrowed book data
    """

    user_id: str
    book_id: str
    days: int

    @validator("user_id")
    def validate_user_id(cls, user_id):
        """
        Validate user_id
        """

        if not frontend_db.Users.find_one({"_id": user_id}):
            logging.error("User not found")
            raise CustomError("User not found", 404)

        return user_id

    @validator("book_id")
    def validate_book_id(cls, book_id):
        """
        Validate book_id
        """

        book = frontend_db.Books.find_one({"_id": book_id})

        if not book:
            logging.error("Book not found")
            raise CustomError("Book not found", 404)

        if book.get("is_borrowed") is True:
            logging.error("Book has already been borrowed")
            raise CustomError("Book has already been borrowed", 400)

        return book_id


class ReturnedBookSchema(BaseModel):
    """
    Pydantic schema for returned book data
    """

    book_id: str

    @validator("book_id")
    def validate_book_id(cls, book_id):
        """
        Validate book_id
        """

        book = frontend_db.Books.find_one({"_id": book_id})

        if not book:
            logging.error("Book not found")
            raise CustomError("Book not found", 404)

        if book.get("is_borrowed") is False:
            logging.error("Book has not been borrowed")
            raise CustomError("Book has not been borrowed", 400)

        return book_id
