import re
from typing import List, Any, Annotated, Callable

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from pydantic_core import core_schema


class _ObjectIdPydanticAnnotation:
    # Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types.

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            return ObjectId(input_value)

        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )


PyObjectId = Annotated[
    ObjectId, _ObjectIdPydanticAnnotation
]


class Item(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    model_config = ConfigDict(populate_by_name=True)


class Items(BaseModel):
    items: List[Item]


class Email:
    email: str

    def __post_init__(self):
        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email address.")


class Student(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)

    def get_name(self):
        return ' '.join([self.first_name, self.last_name])
