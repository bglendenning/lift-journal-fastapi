from typing_extensions import Self

from lift_journal_data.schemas.user import UserSchema
from pydantic import field_validator, model_validator, ValidationInfo


class UserCreateSchema(UserSchema):
    password2: str

    class Config:
        from_attributes = True

    @field_validator("password", "password2")
    @classmethod
    def check_empty(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            raise ValueError(f"{info.field_name} cannot be empty")

        return value

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        password = self.password
        password2 = self.password2

        if password != password2:
            raise ValueError("Passwords do not match")

        return self
