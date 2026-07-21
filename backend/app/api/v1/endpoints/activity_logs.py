from app.api.dependencies.query import QueryParameters, get_query_parameters
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import RoleEnum
from app.schemas.base import PagedResponse
from app.schemas.activity_log import ActivityLogResponse
from app.services import activity_log

router = APIRouter()

@router.get("/", response_model=PagedResponse[ActivityLogResponse])
def read_activity_logs(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    items = activity_log.get_multi(db, params=params)
    total = activity_log.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}
