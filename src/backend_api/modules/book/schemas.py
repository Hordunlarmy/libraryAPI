from datetime import datetime

from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    title: str
    author: str
    category: str
    publisher: str


class BookSchema(BookCreateSchema):
    id: str


class UnavailableBook(BaseModel):
    id: str
    title: str
    author: str
    publisher: str
    category: str
    available_on: datetime
