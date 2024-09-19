from shared.database import Database, db
from modules.user.schemas import UserSchema, User, Book
from shared.broker import SyncManager
from shared.logger import logging


broker = SyncManager()


class UserManager:
    """
    class to manage user data
    """

    def __init__(self, database: Database = db):
        self.db = database

    def sync_user(self, user_data):
        """
        Sync user data asynchronously.
        """

        query = """
        INSERT INTO Users (id, email, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        """

        params = (
            user_data.get("_id"),
            user_data.get("email"),
            user_data.get("first_name"),
            user_data.get("last_name"),
        )

        try:
            self.db.commit(query, params)
            return {"message": "User synced successfully"}
        except Exception as e:
            logging.error(f"Error syncing user: {e}")
            return {"error": f"Error syncing user: {str(e)}"}, 500

    async def get_user(self, user_id: str) -> UserSchema:
        """
        Get user data
        """

        query = """
        SELECT * FROM Users
        WHERE id = %s
        """

        params = (user_id,)

        user_data = self.db.select(query, params)

        return user_data

    async def get_all_users(self) -> list[UserSchema]:
        """
        Get all users
        """

        query = """
        SELECT * FROM Users
        """

        users_data = self.db.select(query)

        return [UserSchema(**user_data) for user_data in users_data]

    async def get_users_and_books_borrowed(self) -> list[User]:
        """
        Get users and books borrowed
        """

        query = """
        SELECT Users.id AS user_id, Users.email, Users.first_name, 
        Users.last_name, Books.id AS book_id, Books.title, Books.author, 
        Books.publisher, Books.category
        FROM Users
        JOIN BorrowedBooks ON Users.id = BorrowedBooks.user_id
        JOIN Books ON BorrowedBooks.book_id = Books.id
        """

        users_books_data = self.db.select(query)

        # Process the data
        users_dict = {}
        for record in users_books_data:
            user_id = record["user_id"]
            book_info = Book(
                book_id=record["book_id"],
                title=record["title"],
                author=record["author"],
                publisher=record["publisher"],
                category=record["category"],
            )

            # If the user is not already in the result dictionary, add them
            if user_id not in users_dict:
                users_dict[user_id] = User(
                    user_id=user_id,
                    email=record["email"],
                    first_name=record["first_name"],
                    last_name=record["last_name"],
                    books=[book_info],  # Initialize with the current book
                )
            else:
                # Append the book info to the existing user's list of books
                users_dict[user_id].books.append(book_info)

        # Create a UsersBooksResponse object to return
        response = [
            User(**user_data.dict()) for user_data in users_dict.values()
        ]
        return response
