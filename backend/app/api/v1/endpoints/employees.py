from app.schemas.response import ActionResponse
from app.api.dependencies.query import QueryParameters, get_query_parameters
from app.schemas.workflow_history import WorkflowHistoryResponse
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
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

