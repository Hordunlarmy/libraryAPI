# test_book_endpoints.py
from unittest.mock import patch

import pytest
from flask import jsonify
from modules.book.manager import BookManager
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
def client(app):
    """
    Initialize a test client for the Flask app.
    """
    return app.test_client()


@pytest.fixture
def mocked_uuid():
    """Fixture for generating a mocked UUID."""

    book_uuid1 = generate_uuid()
    book_uuid2 = generate_uuid()
    return book_uuid1, book_uuid2


@pytest.fixture
def book_manager(mock_db):
    """Initializes the BookManager with a mock database"""

    return BookManager(db=mock_db)


@pytest.fixture
def book_data(mocked_uuid):
    """Fixture to provide mock book data."""

    id_1, id_2 = mocked_uuid
    return [
        {
            "_id": id_1,
            "title": "Test Book 1",
            "author": "Test Author 1",
            "is_borrowed": False,
            "publisher": "Publisher1",
            "category": "Category1",
            "created_at": "Thu, 19 Sep",
        },
        {
            "_id": id_2,
            "title": "Test Book 2",
            "author": "Test Author 2",
            "is_borrowed": True,
            "publisher": "Publisher2",
            "category": "Category2",
            "created_at": "Thu, 19 Sep",
        },
    ]


def test_list_available_books(client, app, book_data):
    """Test the /books/available endpoint."""

    with app.app_context():
        with patch.object(
            BookManager,
            "list_all_available_books",
            return_value=(jsonify(book_data), 200),
        ):
            response = client.get("/api/books/available")
            assert response.status_code == 200
            assert response.get_json() == book_data


def test_get_book_by_id(client, app, book_data):
    """Test the /books/<id> endpoint."""

    with app.app_context():
        with patch.object(
            BookManager,
            "get_book_by_id",
            return_value=(jsonify(book_data[0]), 200),
        ):
            response = client.get(f"/api/books/{book_data[0]['_id']}")
            assert response.status_code == 200
            assert response.get_json() == book_data[0]


def test_filter_books(client, app, book_data):
    """Test the /books/filter endpoint."""

    with app.app_context():
        with patch.object(
            BookManager,
            "filter_books",
            return_value=(jsonify(book_data[1]), 200),
        ):
            response = client.post(
                "/api/books/filter",
                query_string={
                    "publishers": "Publisher2",
                    "categories": "Category2",
                },
            )
            assert response.status_code == 200
            assert response.get_json() == book_data[1]
