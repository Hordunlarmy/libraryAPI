from unittest.mock import MagicMock, patch

import pytest
from main import app
from modules.user.manager import UserManager
from modules.user.schemas import UserSchema
from pymongo.errors import DuplicateKeyError
from shared.error_handler import CustomError
from shared.logger import logging
from shared.utils import generate_uuid


@pytest.fixture
def mocked_uuid():
    """Fixture for generating a mocked UUID."""

    return generate_uuid()


@pytest.fixture
def user_data():
    """
    Fixture for generating user data.
    """

    return UserSchema(
        email="test@example.com", first_name="Test", last_name="User"
    )


@pytest.fixture
def mock_db(mocked_uuid):
    """Mocks the MongoDB database."""

    mock_db = MagicMock()
    mock_db.Users.insert_one.return_value.inserted_id = mocked_uuid
    return mock_db


@pytest.fixture
def user_manager(mock_db):
    """Initializes the UserManager with a mock database."""
    return UserManager(db=mock_db)


def test_enroll_user_success(user_manager, user_data, mocked_uuid, mock_db):
    """Test successful user enrollment."""

    mock_broker = MagicMock()

    with patch("modules.user.manager.broker", mock_broker), patch(
        "modules.user.manager.generate_uuid", return_value=mocked_uuid
    ):
        with app.app_context():
            response, status_code = user_manager.enroll_user(user_data)

            logging.info(f"Mocked UUID: {mocked_uuid}")
            logging.info(f"Actual UUID: {response.get_json().get('user_id')}")

            assert status_code == 201
            assert response.get_json() == {"user_id": mocked_uuid}

            mock_db.Users.insert_one.assert_called_once_with(
                {
                    "_id": mocked_uuid,
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "action": "enroll_user",
                }
            )
            mock_broker.publish.assert_called_once()


def test_enroll_user_duplicate_key_error(user_manager, user_data, mock_db):
    """Test handling of DuplicateKeyError during enrollment."""

    mock_db.Users.insert_one.side_effect = DuplicateKeyError(
        "duplicate key error"
    )

    with app.app_context():
        with pytest.raises(CustomError) as exc_info:
            user_manager.enroll_user(user_data)

        assert exc_info.value.http_status_code == 400
        assert str(exc_info.value.message) == "User already exists"

        mock_db.Users.insert_one.assert_called_once()


def test_enroll_user_database_exception(user_manager, user_data, mock_db):
    """Test handling of general database exception."""

    mock_db.Users.insert_one.side_effect = Exception("Database error")

    with app.app_context():
        with pytest.raises(CustomError) as exc_info:
            user_manager.enroll_user(user_data)

            assert exc_info.value.http_status_code == 500
            assert str(exc_info.value.message) == "Database error"


def test_enroll_user_broker_error_rollback_performed(
    user_manager, user_data, mock_db, mocked_uuid
):
    """
    Test handling of message broker error and successful database rollback.
    """

    mock_broker = MagicMock()
    mock_broker.publish.side_effect = Exception("Broker error")

    with patch("modules.user.manager.broker", mock_broker), patch(
        "modules.user.manager.generate_uuid", return_value=mocked_uuid
    ):
        with app.app_context():
            with pytest.raises(CustomError) as exc_info:
                user_manager.enroll_user(user_data)

                assert exc_info.value.http_status_code == 400
                assert (
                    str(exc_info.value.message)
                    == "User enrollment failed. Try again."  # noqa
                )

            mock_broker.publish.assert_called_once()

            mock_db.Users.insert_one.assert_called_once()

            mock_db.Users.delete_one.assert_called_once_with(
                {"_id": mocked_uuid}
            )
