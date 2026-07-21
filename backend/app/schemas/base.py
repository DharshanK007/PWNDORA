from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel

T = TypeVar("T")

class PagedResponse(BaseModel, Generic[T]):
    items: Sequence[T]
    total: int
    skip: int
    limit: int


class WorkflowMetadataResponse(BaseModel):
    current_state: str
    allowed_transitions: list[str]

