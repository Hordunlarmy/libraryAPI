# test_book_manager.py
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from main import app
from modules.book.manager import BookManager
from shared.error_handler import CustomError
from shared.utils import generate_uuid


@pytest.fixture
def mock_db():
    """Mocks the database for testing."""

    mock_db = MagicMock()
    mock_db.Books = MagicMock()
    mock_db.Users = MagicMock()
    mock_db.BorrowedBooks = MagicMock()
    return mock_db


@pytest.fixture
def mock_schema():
    """Mocks the schema for testing."""

    mock_schema = MagicMock()
    mock_schema.BorrowedBookSchema = MagicMock()
    mock_schema.ReturnedBookSchema = MagicMock()
    return mock_schema


@pytest.fixture
def mocked_uuid():
    """Fixture for generating a mocked UUID."""

    uuid1 = generate_uuid()
    uuid2 = generate_uuid()

    return uuid1, uuid2


@pytest.fixture
def book_manager(mock_db):
    """Initializes the BookManager with a mock database"""

    return BookManager(db=mock_db)


@pytest.fixture
def book_data(mocked_uuid):
    """Fixture for book data."""

    uuid1, uuid2 = mocked_uuid

    return [
        {
            "_id": uuid1,
            "author": "Author1",
            "category": "Category1",
            "created_at": datetime.utcnow().isoformat(),
            "is_borrowed": False,
            "publisher": "Publisher1",
            "title": "Book1",
        },
        {
            "_id": uuid2,
            "author": "Author2",
            "category": "Category2",
            "created_at": datetime.utcnow().isoformat(),
            "is_borrowed": True,
            "publisher": "Publisher2",
            "title": "Book2",
        },
    ]


def test_sync_book_add_success(book_manager, mock_db):
    """Test successful addition of a book."""

    with app.app_context():
        book_data = {
            "action": "add_book",
            "author": "Author1",
            "category": "Category1",
            "publisher": "Publisher1",
            "title": "Book1",
        }

        response = book_manager.sync_book(book_data)

        mock_db.Books.insert_one.assert_called_once()
        assert response[1] == 200
        assert "Book synced successfully" in response[0].json["message"]


def test_list_all_available_books(book_manager, mock_db, book_data):
    """
    Test listing all available books.
    """

    with app.app_context():
        mock_db.Books.find.return_value = [book_data[0]]

        response = book_manager.list_all_available_books()

        mock_db.Books.find.assert_called_once_with({"is_borrowed": False})
        assert response[1] == 200
        assert len(response[0].json) == 1
        assert response[0].json[0]["title"] == "Book1"


def test_get_book_by_id_success(book_manager, mock_db, mocked_uuid, book_data):
    """
    Test getting a book by its ID.
    """

    with app.app_context():
        uuid1, uuid2 = mocked_uuid
        mock_db.Books.find_one.return_value = book_data[0]

        response = book_manager.get_book_by_id(uuid1)

        mock_db.Books.find_one.assert_called_once_with({"_id": uuid1})
        assert response[1] == 200
        assert response[0].json["title"] == "Book1"


def test_borrow_book_success(book_manager, mocked_uuid, mock_db, mock_schema):
    """
    Test successful borrowing of a book.
    """

    mock_broker = MagicMock()

    with patch("modules.book.manager.broker", mock_broker):
        with app.app_context():
            uuid1, uuid2 = mocked_uuid

            mock_db.Users.find_one.return_value = {"_id": uuid2}
            mock_db.Books.find_one.return_value = {
                "_id": uuid1,
                "title": "Test Book",
                "is_borrowed": False,
            }

            # Mocking the schema behavior and return value as an object
            mock_borrowed_book_data = MagicMock()
            mock_borrowed_book_data.dict.return_value = {
                "user_id": uuid2,
                "book_id": uuid1,
                "days": 7,
            }

            # Mock the schema to return the object with .dict() method
            mock_schema.BorrowedBookSchema.return_value.load.return_value = (
                mock_borrowed_book_data
            )

            borrow_data = mock_schema.BorrowedBookSchema.return_value.load(
                {"user_id": uuid2, "book_id": uuid1, "days": 7}
            )
            response = book_manager.borrow_book(borrow_data)

            mock_db.BorrowedBooks.insert_one.assert_called_once()
            mock_db.Books.update_one.assert_called_once_with(
                {"_id": uuid1}, {"$set": {"is_borrowed": True}}
            )
            assert response[1] == 200
            assert "Book borrowed successfully" in response[0].json["message"]


def test_borrow_book_failure_rollbacks(
    book_manager, mocked_uuid, mock_db, mock_schema
):
    """
    Test failing to borrow a book.
    """

    mock_broker = MagicMock()

    with patch("modules.book.manager.broker", mock_broker):

        with app.app_context():
            uuid1, uuid2 = mocked_uuid

            mock_db.Users.find_one.return_value = {"_id": uuid2}
            mock_db.Books.find_one.return_value = {
                "_id": uuid1,
                "title": "Test Book",
                "is_borrowed": False,
            }

            mock_borrowed_book_data = MagicMock()
            mock_borrowed_book_data.dict.return_value = {
                "user_id": uuid2,
                "book_id": uuid1,
                "days": 7,
            }

            mock_schema.BorrowedBookSchema.return_value.load.return_value = (
                mock_borrowed_book_data
            )

            borrow_data = mock_schema.BorrowedBookSchema.return_value.load(
                {"user_id": uuid2, "book_id": uuid1, "days": 7}
            )

            mock_db.Books.update_one = MagicMock()
            mock_db.BorrowedBooks.insert_one = MagicMock()

            mock_broker.publish.side_effect = Exception("Publish failed")

            with pytest.raises(
                CustomError, match="Failed to borrow book. Try again."
            ):
                book_manager.borrow_book(borrow_data)

            mock_db.Books.update_one.assert_any_call(
                {"_id": uuid1}, {"$set": {"is_borrowed": True}}
            )

            assert mock_db.Books.update_one.call_count == 2
            mock_db.Books.update_one.assert_any_call(
                {"_id": uuid1}, {"$set": {"is_borrowed": False}}
            )

            mock_db.BorrowedBooks.insert_one.assert_called_once()


def test_return_book_success(book_manager, mock_db, mocked_uuid, mock_schema):
    """
    Test successful return of a book.
    """

    mock_broker = MagicMock()

    with patch("modules.book.manager.broker", mock_broker):

        with app.app_context():
            uuid1, uuid2 = mocked_uuid

            mock_db.Books.find_one.return_value = {
                "_id": uuid1,
                "title": "Test Book",
                "is_borrowed": True,
            }

            mock_returned_book_data = MagicMock()
            mock_returned_book_data.dict.return_value = {
                "book_id": uuid1,
            }

            mock_schema.BorrowedBookSchema.return_value.load.return_value = (
                mock_returned_book_data
            )

            response = book_manager.return_book(mock_returned_book_data)

            mock_db.BorrowedBooks.delete_one.assert_called_once_with(
                {"book_id": uuid1}
            )
            mock_db.Books.update_one.assert_called_once_with(
                {"_id": uuid1}, {"$set": {"is_borrowed": False}}
            )

            assert response[1] == 200
            assert "Book returned successfully" in response[0].json["message"]


def test_filter_books_by_category(book_manager, mock_db, book_data):
    """
    Test filtering books by category.
    """

    with app.app_context():
        mock_db.Books.find.return_value = [book_data[0]]

        response = book_manager.filter_books(categories=["Category1"])

        mock_db.Books.find.assert_called_once_with(
            {"category": {"$in": ["Category1"]}}
        )
        assert response[1] == 200
        assert len(response[0].json) == 1
        assert response[0].json[0]["title"] == "Book1"


def test_filter_books_by_publisher(book_manager, mock_db, book_data):
    """
    Test filtering books by publisher.
    """

    with app.app_context():
        mock_db.Books.find.return_value = [book_data[0]]

        response = book_manager.filter_books(publishers=["Publisher1"])

        mock_db.Books.find.assert_called_once_with(
            {"publisher": {"$in": ["Publisher1"]}}
        )
        assert response[1] == 200
        assert len(response[0].json) == 1
        assert response[0].json[0]["title"] == "Book1"
