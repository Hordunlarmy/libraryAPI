import json

from decouple import config
from flask import jsonify
from modules.user.schemas import UserSchema
from pymongo.errors import DuplicateKeyError
from shared.broker import SyncManager
from shared.database import db as frontend_db
from shared.error_handler import CustomError
from shared.logger import logging
from shared.utils import generate_uuid

broker = SyncManager()


class UserManager:
    """
    class to manage user operations
    """

    def __init__(
        self,
        db=frontend_db,
        pub_queue: str = config("BROKER_PUB_QUEUE"),
    ):
        """
        class initialization phase(initialized with database)
        """

        self.db = db
        self.pub_queue = pub_queue

    def enroll_user(self, user_data: UserSchema):
        """
        Method to enroll a user into the system and publish user data to a
        message broker.
        """

        user_data = user_data.dict()
        user_data["_id"] = generate_uuid()

        try:
            user_id = self.db.Users.insert_one(user_data).inserted_id
            logging.info(f"User {user_id} enrolled successfully.")

        except DuplicateKeyError as e:
            logging.error(f"Duplicate key error: {e}")
            raise CustomError("User already exists", 400) from e

        except Exception as e:
            logging.error(f"Error enrolling user: {e}")
            raise CustomError("Error enrolling user", 500) from e

        try:
            user_data["action"] = "enroll_user"
            user_data_json = json.dumps(user_data)

            broker.publish(user_data_json, self.pub_queue)
            logging.info(
                f"User data published to broker queue {self.pub_queue}."
            )

            return jsonify({"user_id": str(user_id)}), 201

        except Exception as e:
            logging.error(f"Error publishing user data to broker: {e}")
            try:
                self.db.Users.delete_one({"_id": user_id})
                logging.info(f"Rolled back user {user_id} from database.")
            except Exception as rollback_error:
                logging.error(f"Error during rollback: {rollback_error}")
            raise CustomError("User enrollment failed. Try again.", 500) from e
