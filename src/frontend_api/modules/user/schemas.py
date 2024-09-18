from pydantic import BaseModel, validator


class InvalidEmailError(Exception):
    """
    Custom exception for invalid email
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserSchema(BaseModel):
    """
    Pydantic schema for user data
    """

    email: str
    first_name: str
    last_name: str

    @validator("email")
    def email_must_contain_atsign(cls, v):
        if "@" not in v:
            raise InvalidEmailError("Email must contain an '@' sign")
        return v
