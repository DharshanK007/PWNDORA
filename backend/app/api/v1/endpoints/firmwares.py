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
from app.schemas.firmware import FirmwareCreate, FirmwareUpdate, FirmwareResponse
from app.services import firmware

router = APIRouter()

@router.get("/", response_model=PagedResponse[FirmwareResponse])
def read_firmwares(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve firmwares.
    """
    items = firmware.get_multi(db, params=params)
    total = firmware.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.post("/", response_model=FirmwareResponse, status_code=status.HTTP_201_CREATED)
def create_firmware(
    *,
    db: Session = Depends(deps.get_db),
    item_in: FirmwareCreate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    """
    Create new firmware.
    """
    item = firmware.create(db, obj_in=item_in)
    return item

@router.put("/{id}", response_model=FirmwareResponse)
def update_firmware(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: FirmwareUpdate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    """
    Update an existing firmware.
    """
    item = firmware.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Firmware not found")
    item = firmware.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/{id}", response_model=FirmwareResponse)
def read_firmware(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get firmware by ID.
    """
    item = firmware.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Firmware not found")
    return item

@router.delete("/{id}", response_model=FirmwareResponse)
def delete_firmware(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    """
    Delete a firmware.
    """
    item = firmware.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Firmware not found")
    item = firmware.remove(db, id=id)
    return item


@router.post("/{id}/submit", response_model=ActionResponse[FirmwareResponse])
def submit_firmware_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = firmware.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Firmware not found")
    return ActionResponse(success=True, message='Action successful', data=firmware.submit(db, db_obj=item))

@router.post("/{id}/approve", response_model=ActionResponse[FirmwareResponse])
def approve_firmware_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    item = firmware.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Firmware not found")
    return ActionResponse(success=True, message='Action successful', data=firmware.approve(db, db_obj=item))

@router.post("/{id}/deploy", response_model=ActionResponse[FirmwareResponse])
def deploy_firmware_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = firmware.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Firmware not found")
    return ActionResponse(success=True, message='Action successful', data=firmware.deploy(db, db_obj=item))


WORKFLOW_ACTIONS = {
    "Draft": ["submit"],
    "Pending Approval": ["approve"],
    "Approved": ["deploy"],
    "Deployed": ["rollback"],
    "Retired": []
}

@router.get("/{id}/workflow", response_model=WorkflowMetadataResponse)
def get_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    item = firmware.get(db, id=id)
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
    return WorkflowHistoryService.get_history_for_entity(db, "firmwares", str(id))

