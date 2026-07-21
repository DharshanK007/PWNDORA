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
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.services import inventory

router = APIRouter()

@router.get("/", response_model=PagedResponse[InventoryResponse])
def read_inventory(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve inventory.
    """
    items = inventory.get_multi(db, params=params)
    total = inventory.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventor(
    *,
    db: Session = Depends(deps.get_db),
    item_in: InventoryCreate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Create new inventor.
    """
    item = inventory.create(db, obj_in=item_in)
    return item

@router.put("/{id}", response_model=InventoryResponse)
def update_inventor(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: InventoryUpdate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Update an existing inventor.
    """
    item = inventory.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    item = inventory.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/{id}", response_model=InventoryResponse)
def read_inventor(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get inventor by ID.
    """
    item = inventory.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return item

@router.delete("/{id}", response_model=InventoryResponse)
def delete_inventor(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Delete a inventor.
    """
    item = inventory.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    item = inventory.remove(db, id=id)
    return item


from pydantic import BaseModel
class QuantityRequest(BaseModel):
    quantity: int

@router.post("/{id}/allocate", response_model=ActionResponse[InventoryResponse])
def allocate_inventory_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    req: QuantityRequest,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER, RoleEnum.ENGINEER]))
) -> Any:
    item = inventory.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return ActionResponse(success=True, message='Action successful', data=inventory.allocate(db, db_obj=item, quantity=req.quantity))

@router.post("/{id}/consume", response_model=ActionResponse[InventoryResponse])
def consume_inventory_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER, RoleEnum.ENGINEER]))
) -> Any:
    item = inventory.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return ActionResponse(success=True, message='Action successful', data=inventory.consume(db, db_obj=item))


WORKFLOW_ACTIONS = {
    "Created": ["allocate"],
    "Available": ["allocate"],
    "Restocked": ["allocate"],
    "Allocated": ["consume"],
    "Consumed": []
}

@router.get("/{id}/workflow", response_model=WorkflowMetadataResponse)
def get_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    item = inventory.get(db, id=id)
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
    return WorkflowHistoryService.get_history_for_entity(db, "inventory", str(id))

