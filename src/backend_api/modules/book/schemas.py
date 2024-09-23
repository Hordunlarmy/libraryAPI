from datetime import datetime

from pydantic import BaseModel, constr, validator
from shared.error_handler import CustomError


class BookCreateSchema(BaseModel):
    title: constr(min_length=1)
    author: constr(min_length=1)
    category: constr(min_length=1)
    publisher: constr(min_length=1)

    @validator("title")
    def title_must_be_string_and_not_empty(cls, v):
        if not isinstance(v, str) or not v:
            raise CustomError("Title must be a non-empty string.", 400)
        return v

    @validator("author")
    def author_must_be_string_and_not_empty(cls, v):
        if not isinstance(v, str) or not v:
            raise CustomError("Author must be a non-empty string.", 400)
        return v

    @validator("category")
    def category_must_be_string_and_not_empty(cls, v):
        if not isinstance(v, str) or not v:
            raise CustomError("Category must be a non-empty string.", 400)
        return v

    @validator("publisher")
    def publisher_must_be_string_and_not_empty(cls, v):
        if not isinstance(v, str) or not v:
            raise CustomError("Publisher must be a non-empty string.", 400)
        return v


class BookSchema(BookCreateSchema):
    id: str


class UnavailableBook(BaseModel):
    id: str
    title: str
    author: str
    publisher: str
    category: str
    available_on: datetime
