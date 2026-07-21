from app.api.dependencies.query import QueryParameters, get_query_parameters
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.models.user import RoleEnum
from app.schemas.base import PagedResponse
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.services import department

router = APIRouter()

@router.get("/", response_model=PagedResponse[DepartmentResponse])
def read_departments(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve departments.
    """
    items = department.get_multi(db, params=params)
    total = department.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    *,
    db: Session = Depends(deps.get_db),
    item_in: DepartmentCreate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Create new department.
    """
    item = department.create(db, obj_in=item_in)
    return item

@router.put("/{id}", response_model=DepartmentResponse)
def update_department(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: DepartmentUpdate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Update an existing department.
    """
    item = department.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    item = department.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/{id}", response_model=DepartmentResponse)
def read_department(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get department by ID.
    """
    item = department.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    return item

@router.delete("/{id}", response_model=DepartmentResponse)
def delete_department(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Delete a department.
    """
    item = department.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    item = department.remove(db, id=id)
    return item
