from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    User create schema
    """

    id: str
    email: str
    first_name: str
    last_name: str
    created_at: Optional[datetime]


class Book(BaseModel):
    book_id: str
    title: str
    author: str
    publisher: str
    category: str


class User(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: str
    books: List[Book] = []
