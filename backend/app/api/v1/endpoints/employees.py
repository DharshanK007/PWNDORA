from app.schemas.response import ActionResponse
from app.api.dependencies.query import QueryParameters, get_query_parameters
from app.schemas.workflow_history import WorkflowHistoryResponse
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.models.user import RoleEnum
from app.schemas.base import PagedResponse, WorkflowMetadataResponse
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services import employee

router = APIRouter()

@router.get("/", response_model=PagedResponse[EmployeeResponse])
def read_employees(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve employees.
    """
    items = employee.get_multi(db, params=params)
    total = employee.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    *,
    db: Session = Depends(deps.get_db),
    item_in: EmployeeCreate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Create new employee.
    """
    item = employee.create(db, obj_in=item_in)
    return item

@router.put("/{id}", response_model=EmployeeResponse)
def update_employee(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: EmployeeUpdate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Update an existing employee.
    """
    item = employee.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Employee not found")
    item = employee.update(db, db_obj=item, obj_in=item_in)
    return item

# ─────────────────────────────────────────────────────────────────────────────
# SE Stage 4: Employee Export with Stolen Internal Service Key Bypass
# ─────────────────────────────────────────────────────────────────────────────
_SE_INTERNAL_SVC_KEY = "nf-internal-svc-x9k2p"

@router.get("/export")
def export_all_employees(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Full employee PII bulk export.
    Intended to require Administrator role.
    Deliberately contains a second authorization path that accepts the internal
    service key stolen in SE Stage 3 — the real payoff of credential exfiltration.
    """
    svc_key_header = request.headers.get("X-Service-Key", "")
    is_admin = hasattr(current_user, 'role') and str(current_user.role.value if hasattr(current_user.role, 'value') else current_user.role) in ["ADMINISTRATOR", "Administrator"]
    key_bypass = _SE_INTERNAL_SVC_KEY in svc_key_header

    if not is_admin and not key_bypass:
        raise HTTPException(status_code=403, detail="Insufficient privileges. Admin access required.")

    # Fetch full unredacted employee list
    from app.api.dependencies.query import QueryParameters
    from app.schemas.employee import EmployeeResponse
    items = employee.get_multi(db, params=QueryParameters(skip=0, limit=10000))

    # Outcome-based gate: export was reached by a non-admin using the stolen key
    stolen_key_export = key_bypass and not is_admin
    from app.scenarios.stage_gate import advance_if_stage_matches
    advance_if_stage_matches(
        db, "GET /api/v1/employees/export",
        {"stolen_key_export": stolen_key_export}
    )

    return {
        "items": items,
        "total": len(items),
        "export_method": "service_key_bypass" if stolen_key_export else "admin_authorized",
        "classification": "SENSITIVE — Full Employee PII"
    }

@router.get("/{id}", response_model=EmployeeResponse)
def read_employee(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get employee by ID.
    """
    item = employee.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    # Stage Gate: Stage 2 IDOR check for Operation Phantom Firmware
    from app.scenarios.stage_gate import advance_if_stage_matches
    advance_if_stage_matches(db, "GET /api/v1/employees/{id}", {"employee_id": str(id), "employee_name": f"{item.first_name} {item.last_name}"})
    
    return item

@router.delete("/{id}", response_model=EmployeeResponse)
def delete_employee(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Delete a employee.
    """
    item = employee.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Employee not found")
    item = employee.remove(db, id=id)
    return item


@router.post("/{id}/activate", response_model=ActionResponse[EmployeeResponse])
def activate_employee_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = employee.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Employee not found")
    return ActionResponse(success=True, message='Action successful', data=employee.activate(db, db_obj=item))

@router.post("/{id}/terminate", response_model=ActionResponse[EmployeeResponse])
def terminate_employee_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = employee.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Employee not found")
    return ActionResponse(success=True, message='Action successful', data=employee.terminate(db, db_obj=item))


# ─────────────────────────────────────────────────────────────────────────────
# SE Stage 4: Employee Export with Stolen Internal Service Key Bypass
# ─────────────────────────────────────────────────────────────────────────────
# The stolen internal API key from Stage 3. This is the exact key value the
# learner reads out of /app/internal_secrets/svc_credentials.txt via path traversal.
# It's not a magic string invented for this puzzle — it's the payoff of the
# actual theft from the previous stage.
_SE_INTERNAL_SVC_KEY = "nf-internal-svc-x9k2p"

@router.get("/export")
def export_all_employees(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Full employee PII bulk export.
    Intended to require Administrator role.
    Deliberately contains a second authorization path that accepts the internal
    service key stolen in SE Stage 3 — the real payoff of credential exfiltration.
    """
    svc_key_header = request.headers.get("X-Service-Key", "")
    is_admin = hasattr(current_user, 'role') and str(current_user.role.value if hasattr(current_user.role, 'value') else current_user.role) in ["ADMINISTRATOR", "Administrator"]
    key_bypass = svc_key_header == _SE_INTERNAL_SVC_KEY

    if not is_admin and not key_bypass:
        raise HTTPException(status_code=403, detail="Insufficient privileges. Admin access required.")

    # Fetch full unredacted employee list
    from app.api.dependencies.query import QueryParameters
    from app.schemas.employee import EmployeeResponse
    items = employee.get_multi(db, params=QueryParameters(skip=0, limit=10000))

    # Outcome-based gate: export was reached by a non-admin using the stolen key
    stolen_key_export = key_bypass and not is_admin
    from app.scenarios.stage_gate import advance_if_stage_matches
    advance_if_stage_matches(
        db, "GET /api/v1/employees/export",
        {"stolen_key_export": stolen_key_export}
    )

    return {
        "items": items,
        "total": len(items),
        "export_method": "service_key_bypass" if stolen_key_export else "admin_authorized",
        "classification": "SENSITIVE — Full Employee PII"
    }


WORKFLOW_ACTIONS = {
    "Pending": ["activate", "terminate"],
    "Active": ["suspend", "terminate"],
    "Suspended": ["activate", "terminate"],
    "Terminated": []
}

@router.get("/{id}/workflow", response_model=WorkflowMetadataResponse)
def get_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    item = employee.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Entity not found")
    allowed = WORKFLOW_ACTIONS.get(item.status.value, [])
    return {
        "current_state": item.status.value,
        "allowed_transitions": allowed
    }



@router.get("/{id}/history", response_model=List[WorkflowHistoryResponse])
def get_history(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    from app.services.workflow_history import WorkflowHistoryService
    return WorkflowHistoryService.get_history_for_entity(db, "employees", str(id))

