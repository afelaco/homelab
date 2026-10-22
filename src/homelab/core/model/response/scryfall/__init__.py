from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ScryfallResponseModel(BaseModel, Generic[T]):
    next_page: Optional[str] = None
    data: list[T]
