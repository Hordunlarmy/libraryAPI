from flask import Blueprint
from modules.user.manager import UserManager
from shared.logger import logging  # noqa
from modules.user.schemas import UserSchema
from shared.error_handler import error_handler

user_manager = UserManager()
user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/enroll", strict_slashes=False, methods=["POST"])
@error_handler(schema=UserSchema)
def enroll_user(user_data):
    """
    endpoint to enroll a user
    """

    response, status_code = user_manager.enroll_user(user_data)

    return response, status_code
