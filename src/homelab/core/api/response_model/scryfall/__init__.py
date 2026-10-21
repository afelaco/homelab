from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, model_serializer

T = TypeVar("T")


class ScryfallApiResponseModel(BaseModel, Generic[T]):
    has_more: bool
    next_page: Optional[str] = None
    data: list[T]

    @model_serializer
    def serialize(self) -> list[T]:
        return self.data
