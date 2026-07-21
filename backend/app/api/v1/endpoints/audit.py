from app.api.dependencies.query import QueryParameters, get_query_parameters
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.audit import audit_service
from app.audit.audit_schema import AuditLogResponse
from app.schemas.base import PagedResponse
from app.models.user import RoleEnum

router = APIRouter()

@router.get("/", response_model=PagedResponse[AuditLogResponse])
def read_audit_logs(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    """
    Retrieve audit logs. Requires Administrator role.
    """
    items = audit_service.AuditService.get_logs(db, params=params)
    total = len(items) # For now, simple total since we don't have get_count
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.get("/{id}", response_model=AuditLogResponse)
def read_audit_log(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    """
    Get audit log by ID. Requires Administrator role.
    """
    item = audit_service.AuditService.get_log(db, str(id))
    if not item:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return item
