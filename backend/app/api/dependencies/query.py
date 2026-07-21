from fastapi import Query
from typing import Optional
from pydantic import BaseModel

class QueryParameters(BaseModel):
    skip: int = 0
    limit: int = 100
    sort_by: Optional[str] = None
    sort_order: str = "asc"
    search: Optional[str] = None
    status: Optional[str] = None
    created_after: Optional[str] = None
    created_before: Optional[str] = None

class CursorQueryParameters(BaseModel):
    cursor: Optional[str] = None
    limit: int = 100
    sort_order: str = "asc"
    search: Optional[str] = None

def get_query_parameters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = None,
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    search: Optional[str] = None,
    status: Optional[str] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None
) -> QueryParameters:
    return QueryParameters(
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search,
        status=status,
        created_after=created_after,
        created_before=created_before
    )

def get_cursor_query_parameters(
    cursor: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    search: Optional[str] = None
) -> CursorQueryParameters:
    return CursorQueryParameters(
        cursor=cursor,
        limit=limit,
        sort_order=sort_order,
        search=search
    )
