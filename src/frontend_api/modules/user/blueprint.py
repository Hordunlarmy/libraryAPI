from flask import Blueprint, request
from modules.user.manager import UserManager
from modules.user.schemas import UserSchema
from shared.logger import logging  # noqa

user_manager = UserManager()
user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/enroll", strict_slashes=False, methods=["POST"])
def enroll_user():
    """
    endpoint to enroll a user
    """

    user_data = UserSchema(**request.json)

    response, status_code = user_manager.enroll_user(user_data)

    return response, status_code
