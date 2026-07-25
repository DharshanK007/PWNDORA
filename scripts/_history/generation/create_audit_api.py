import os

with open("backend/app/api/v1/endpoints/audit.py", "w") as f:
    f.write('''from typing import Any
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
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    """
    Retrieve audit logs. Requires Administrator role.
    """
    items = audit_service.AuditService.get_logs(db, skip=skip, limit=limit)
    total = len(items) # For now, simple total since we don't have get_count
    return {"items": items, "total": total, "skip": skip, "limit": limit}

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
''')

# Register the router in api.py
api_file = "backend/app/api/v1/api.py"
with open(api_file, "r") as f:
    content = f.read()

if "from app.api.v1.endpoints import audit" not in content:
    content = content.replace(
        "from app.api.v1.endpoints import auth", 
        "from app.api.v1.endpoints import auth\nfrom app.api.v1.endpoints import audit"
    )
    content += '\napi_router.include_router(audit.router, prefix="/audit", tags=["audit"])\n'
    with open(api_file, "w") as f:
        f.write(content)

print("Created audit endpoints.")
