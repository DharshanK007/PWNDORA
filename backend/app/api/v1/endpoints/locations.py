from app.api.dependencies.query import QueryParameters, get_query_parameters
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.models.user import RoleEnum
from app.schemas.base import PagedResponse
from app.schemas.machine_location import MachineLocationCreate, MachineLocationUpdate, MachineLocationResponse
from app.services import machine_location

router = APIRouter()

@router.get("/", response_model=PagedResponse[MachineLocationResponse])
def read_locations(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve locations.
    """
    items = machine_location.get_multi(db, params=params)
    total = machine_location.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.post("/", response_model=MachineLocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(
    *,
    db: Session = Depends(deps.get_db),
    item_in: MachineLocationCreate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Create new location.
    """
    item = machine_location.create(db, obj_in=item_in)
    return item

@router.put("/{id}", response_model=MachineLocationResponse)
def update_location(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: MachineLocationUpdate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Update an existing location.
    """
    item = machine_location.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="MachineLocation not found")
    item = machine_location.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/{id}", response_model=MachineLocationResponse)
def read_location(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get location by ID.
    """
    item = machine_location.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="MachineLocation not found")
    return item

@router.delete("/{id}", response_model=MachineLocationResponse)
def delete_location(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Delete a location.
    """
    item = machine_location.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="MachineLocation not found")
    item = machine_location.remove(db, id=id)
    return item
