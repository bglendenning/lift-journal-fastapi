from typing_extensions import Self

from lift_journal_data.schemas.user import UserSchema
from pydantic import BaseModel, model_validator


class UserCreateSchema(UserSchema):
    password2: str

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        password = self.password
        password2 = self.password2

        if password != password2:
            raise ValueError("Passwords do not match")

        return self


class UserReadSchema(UserSchema):
    email: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
