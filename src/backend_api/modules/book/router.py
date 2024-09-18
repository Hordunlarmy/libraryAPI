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
async def remove_book(book_id: int):
    """
    Remove a book from the database
    """

    return await book_manager.remove_book(book_id)
