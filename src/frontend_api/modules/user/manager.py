from flask import jsonify
from modules.user.schemas import UserSchema
from pymongo.errors import DuplicateKeyError
from shared.database import db as frontend_db
from shared.logger import logging


class UserManager:
    """
    class to manage user operations
    """

    def __init__(self, db=frontend_db):
        """
        class initialization phase(initialized with database)
        """

        self.db = db

    def enroll_user(self, user_data: UserSchema):
        """
        Method to enroll a user
        """

        user_data = user_data.dict()

        try:
            user_id = self.db.Users.insert_one(user_data).inserted_id
            return jsonify({"user_id": str(user_id)}), 201
        except DuplicateKeyError as e:
            logging.error(f"Duplicate key error: {e}")
            return (
                jsonify({"error": "User with this email already exists"}),
                409,
            )
