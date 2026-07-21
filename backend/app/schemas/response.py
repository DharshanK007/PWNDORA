from typing import Generic, TypeVar, Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
import time

T = TypeVar('T')

class PaginationMetadata(BaseModel):
    skip: int
    limit: int
    total: int

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    pagination: PaginationMetadata

class ActionResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    metadata: Dict[str, Any] = {}

    model_config = ConfigDict(arbitrary_types_allowed=True)
