from datetime import datetime

from pydantic import BaseModel, constr, validator


class BookCreateSchema(BaseModel):
    title: constr(min_length=1)
    author: constr(min_length=1)
    category: constr(min_length=1)
    publisher: constr(min_length=1)

    @validator("title")
    def title_must_not_contain_special_chars(cls, v):
        if not v.isalnum():
            raise ValueError(
                "Title must contain only alphanumeric characters."
            )
        return v

    @validator("author")
    def author_must_not_contain_special_chars(cls, v):
        if not v.isalnum():
            raise ValueError(
                "Author must contain only alphanumeric characters."
            )
        return v

    @validator("category")
    def category_must_not_contain_special_chars(cls, v):
        if not v.isalnum():
            raise ValueError(
                "Category must contain only alphanumeric characters."
            )
        return v

    @validator("publisher")
    def publisher_must_not_contain_special_chars(cls, v):
        if not v.isalnum():
            raise ValueError(
                "Publisher must contain only alphanumeric characters."
            )
        return v


class BookSchema(BookCreateSchema):
    id: str

    @validator("id")
    def id_must_be_uuid(cls, v):
        if not v.isalnum():
            raise ValueError("ID must be a valid UUID.")
        return v


class UnavailableBook(BaseModel):
    id: str
    title: str
    author: str
    publisher: str
    category: str
    available_on: datetime
