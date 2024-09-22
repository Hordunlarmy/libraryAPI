from unittest.mock import patch

import pytest
from flask import jsonify
from modules.user.manager import UserManager
from modules.user.schemas import UserSchema
from shared.utils import generate_uuid


@pytest.fixture
def app():
    """
    Initialize the Flask app with testing configuration.
    """

    from main import app

    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app


@pytest.fixture
def mocked_uuid():
    """Fixture for generating a mocked UUID."""

    return generate_uuid()


@pytest.fixture
def client(app):
    """
    Initialize a test client for the Flask app.
    """

    return app.test_client()


@pytest.fixture
def user_data():
    """
    User data fixture for testing.
    """

    return UserSchema(
        email="test@example.com", first_name="Test", last_name="User"
    )


def test_enroll_user_endpoint(client, user_data, app, mocked_uuid):
    """Test the /enroll endpoint integration."""

    with app.app_context():
        with patch.object(
            UserManager,
            "enroll_user",
            return_value=(jsonify({"user_id": mocked_uuid}), 201),
        ):
            response = client.post("/api/users/enroll", json=user_data.dict())
            assert response.status_code == 201
            assert response.get_json() == {"user_id": mocked_uuid}


def test_enroll_user_endpoint_duplicate(client, user_data, app):
    """Test the /enroll endpoint for duplicate user error."""

    with app.app_context():
        with patch.object(
            UserManager,
            "enroll_user",
            return_value=(
                jsonify({"error": "User with this email already exists"}),
                409,
            ),
        ):
            response = client.post("/api/users/enroll", json=user_data.dict())
            assert response.status_code == 409
            assert response.get_json() == {
                "error": "User with this email already exists"
            }


def test_enroll_user_endpoint_server_error(client, user_data, app):
    """Test the /enroll endpoint for server error during enrollment."""

    with app.app_context():
        with patch.object(
            UserManager,
            "enroll_user",
            return_value=(jsonify({"error": "Error enrolling user"}), 500),
        ):
            response = client.post("/api/users/enroll", json=user_data.dict())
            assert response.status_code == 500
            assert response.get_json() == {"error": "Error enrolling user"}
