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
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services import device

router = APIRouter()

@router.get("/", response_model=PagedResponse[DeviceResponse])
def read_devices(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve devices.
    """
    items = device.get_multi(db, params=params)
    total = device.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    *,
    db: Session = Depends(deps.get_db),
    item_in: DeviceCreate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    """
    Create new device.
    """
    item = device.create(db, obj_in=item_in)
    return item

@router.put("/{id}", response_model=DeviceResponse)
def update_device(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: DeviceUpdate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    """
    Update an existing device.
    """
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    item = device.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/{id}", response_model=DeviceResponse)
def read_device(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get device by ID.
    """
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
        
    # Stage Gate: Stage 1 check for Operation Phantom Firmware
    if "PLC-Line2" in item.name or item.asset_group == "Production Line 2":
        from app.scenarios.stage_gate import advance_if_stage_matches
        advance_if_stage_matches(db, str(current_user.id), "GET /api/v1/devices/{id}", {"device_id": str(id)})
        
    return item

@router.delete("/{id}", response_model=DeviceResponse)
def delete_device(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    """
    Delete a device.
    """
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    item = device.remove(db, id=id)
    return item


@router.post("/{id}/register", response_model=ActionResponse[DeviceResponse])
def register_device_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    return ActionResponse(success=True, message='Action successful', data=device.register(db, db_obj=item))

@router.post("/{id}/configure", response_model=ActionResponse[DeviceResponse])
def configure_device_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    return ActionResponse(success=True, message='Action successful', data=device.configure(db, db_obj=item))

@router.post("/{id}/activate", response_model=ActionResponse[DeviceResponse])
def activate_device_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    return ActionResponse(success=True, message='Action successful', data=device.activate(db, db_obj=item))

@router.post("/{id}/decommission", response_model=ActionResponse[DeviceResponse])
def decommission_device_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    return ActionResponse(success=True, message='Action successful', data=device.decommission(db, db_obj=item))

from fastapi import Header

@router.post("/{id}/firmware-push", response_model=ActionResponse[DeviceResponse])
def firmware_push_device_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    x_user_role: str = Header(None, alias="X-User-Role"),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Stage 4 Endpoint — Firmware Push.
    Vulnerable to Client Trust / Session Flaw: reads client-supplied X-User-Role header.
    """
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")

    from app.scenarios.stage_gate import get_active_stage, advance_if_stage_matches
    
    # Option B Gating: Only exploitable if learner is actively on Stage 4
    active_stage = get_active_stage(db, str(current_user.id), "POST /api/v1/devices/{id}/firmware-push")
    
    effective_role = x_user_role or (current_user.role.value if current_user and hasattr(current_user.role, "value") else str(current_user.role))
    
    if active_stage:
        # Gated execution path for active lab session
        advance_if_stage_matches(db, str(current_user.id), "POST /api/v1/devices/{id}/firmware-push", {"role": effective_role, "header_role": x_user_role})
        return ActionResponse(success=True, message="Firmware push executed via privilege escalation!", data=item)
    else:
        # Standard app behavior: require real admin role
        if effective_role not in ["Administrator", "Manager"]:
            raise HTTPException(status_code=403, detail="Insufficient privileges to push firmware.")
        return ActionResponse(success=True, message="Firmware push executed successfully.", data=item)



WORKFLOW_ACTIONS = {
    "New": ["register"],
    "Registered": ["configure"],
    "Configured": ["activate"],
    "Offline": ["activate"],
    "Maintenance": ["configure", "activate"],
    "Online": ["decommission"],
    "Decommissioned": []
}

@router.get("/{id}/workflow", response_model=WorkflowMetadataResponse)
def get_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    item = device.get(db, id=id)
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
    return WorkflowHistoryService.get_history_for_entity(db, "devices", str(id))

