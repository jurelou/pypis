from typing import Any

import pydantic
from pydantic import AnyHttpUrl, EmailStr


class EmailEmptyAllowedStr(EmailStr):
    @classmethod
    def validate(cls, value: str) -> Any:
        """Allow to pass an empty email."""
        if value == "":
            return value
        return super().validate(value)


class AnyHttpUrlEmptyAllowedStr(AnyHttpUrl):
    @classmethod
    def validate(cls, value: str) -> Any:
        """Allow to pass an empty URL."""
        if value == "":
            return value
        return super().validate(value, ...)


class BaseModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True
        orm_mode = True
