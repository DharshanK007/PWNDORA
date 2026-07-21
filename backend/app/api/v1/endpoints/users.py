from app.api.dependencies.query import QueryParameters, get_query_parameters
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.models.user import RoleEnum
from app.schemas.base import PagedResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user

router = APIRouter()

@router.get("/", response_model=PagedResponse[UserResponse])
def read_users(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve users.
    """
    items = user.get_multi(db, params=params)
    total = user.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    item_in: UserCreate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    """
    Create new user.
    """
    item = user.create(db, obj_in=item_in)
    return item

@router.put("/{id}", response_model=UserResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: UserUpdate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    """
    Update an existing user.
    """
    item = user.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    item = user.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/{id}", response_model=UserResponse)
def read_user(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get user by ID.
    """
    item = user.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item

@router.delete("/{id}", response_model=UserResponse)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    """
    Delete a user.
    """
    item = user.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    item = user.remove(db, id=id)
    return item
