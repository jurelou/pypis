import pydantic
from pydantic import EmailStr, AnyHttpUrl

class EmailEmptyAllowedStr(EmailStr):
    @classmethod
    def validate(cls, value: str) -> str:
        if value == "":
            return value
        return super().validate(value)

class AnyHttpUrlEmptyAllowedStr(AnyHttpUrl):
    @classmethod
    def validate(cls, value: str) -> str:
        if value == "":
            return value
        return super().validate(value, ...)


class BaseModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True
        orm_mode = True
