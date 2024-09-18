from shared.database import Database, db
from modules.book.schemas import BookCreateSchema


class BookManager:
    def __init__(self, database: Database = db):
        self.db = database

    async def add_book(self, book_data: BookCreateSchema):
        """
        Add a new book to the database
        """

        query = """
        INSERT INTO Books (title, author, category, publisher)
        VALUES (%s, %s, %s, %s)
        """

        params = (
            book_data.title,
            book_data.author,
            book_data.category,
            book_data.publisher,
        )

        book_id = self.db.execute(query, params)

        return book_id

    async def remove_book(self, book_id: int):
        """
        Remove a book from the database
        """

        query = """
        DELETE FROM Books
        WHERE id = %s
        """

        params = (book_id,)

        self.db.execute(query, params)
