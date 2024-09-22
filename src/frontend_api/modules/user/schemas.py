from pydantic import BaseModel, validator
from shared.error_handler import CustomError


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
            raise CustomError("Invalid email address", 400)
        return v

    @validator("first_name")
    def first_name_must_contain_alpha(cls, v):
        if not v.isalpha():
            raise CustomError("First name must contain only alphabets", 400)
        return v

    @validator("last_name")
    def last_name_must_contain_alpha(cls, v):
        if not v.isalpha():
            raise CustomError("Last name must contain only alphabets", 400)
        return v

    @classmethod
    def validate_fields(cls, values):
        for field in ["email", "first_name", "last_name"]:
            if not values.get(field):
                raise CustomError(
                    f"{field.replace('_', ' ').capitalize()} is required", 400
                )
        return values
