from shared.database import Database, db
from modules.user.schemas import UserSchema
from shared.broker import SyncManager


broker = SyncManager()


class UserManager:
    """
    class to manage user data
    """

    def __init__(self, database: Database = db):
        self.db = database

    async def get_user(self, user_id: str) -> UserSchema:
        """
        Get user data
        """

        query = """
        SELECT email, full_name, last_name
        FROM Users
        WHERE id = %s
        """

        params = (user_id,)

        user_data = self.db.select(query, params)

        return UserSchema(**user_data)

    async def get_all_users(self) -> list[UserSchema]:
        """
        Get all users
        """

        query = """
        SELECT * FROM Users
        """

        users_data = self.db.select(query)

        return [UserSchema(**user_data) for user_data in users_data]
