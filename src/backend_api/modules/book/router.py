from fastapi import APIRouter
from modules.book.manager import BookManager
from modules.book.schemas import BookCreateSchema


book_router = APIRouter(prefix="/api/books")
book_manager = BookManager()


@book_router.post("/add")
async def add_book(book_data: BookCreateSchema):
    """
    Add a new book to the database
    """

    return await book_manager.add_book(book_data)


@book_router.delete("/remove/{book_id}")
async def remove_book(book_id: str):
    """
    Remove a book from the database
    """

    return await book_manager.remove_book(book_id)


@book_router.get("/unavailable")
async def get_unavailable_books():
    """
    Get all unavailable books
    """

    return await book_manager.get_unavailable_books()
