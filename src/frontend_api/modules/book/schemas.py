from bson import ObjectId
from pydantic import BaseModel, validator
from shared.database import db as frontend_db
from shared.logger import logging


class CustomError(Exception):
    """
    Custom exception class for not found errors
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


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

        user_id = ObjectId(user_id)

        if not frontend_db.Users.find_one({"_id": user_id}):
            logging.error("User not found")
            raise CustomError("User not found")

        return user_id

    @validator("book_id")
    def validate_book_id(cls, book_id):
        """
        Validate book_id
        """

        logging.info(f"{book_id=} {type(book_id)}")
        book_id = ObjectId(book_id)

        book = frontend_db.Books.find_one({"_id": book_id})

        if not book:
            logging.error("Book not found")
            raise CustomError("Book not found")

        if book.get("is_borrowed") is True:
            logging.error("Book is already borrowed")
            raise CustomError("Book is already borrowed")

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

        book_id = ObjectId(book_id)

        book = frontend_db.Books.find_one({"_id": book_id})

        if not book:
            logging.error("Book not found")
            raise CustomError("Book not found")

        if book.get("is_borrowed") is False:
            logging.error("Book is not borrowed")
            raise CustomError("Book is not borrowed")

        return book_id
