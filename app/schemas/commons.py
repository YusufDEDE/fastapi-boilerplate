from typing import List, Generic, TypeVar

from pydantic import ConfigDict, BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]

    model_config = ConfigDict(from_attributes=True)
