from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    User create schema
    """

    email: str
    full_name: str
    last_name: str
