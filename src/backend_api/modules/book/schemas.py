from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    title: str
    author: str
    category: str
    publisher: str


class BookSchema(BookCreateSchema):
    id: int
