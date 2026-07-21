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
from app.schemas.maintenance_ticket import MaintenanceTicketCreate, MaintenanceTicketUpdate, MaintenanceTicketResponse
from app.services import maintenance_ticket

router = APIRouter()

@router.get("/", response_model=PagedResponse[MaintenanceTicketResponse])
def read_tickets(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve tickets.
    """
    items = maintenance_ticket.get_multi(db, params=params)
    total = maintenance_ticket.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.post("/", response_model=MaintenanceTicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    *,
    db: Session = Depends(deps.get_db),
    item_in: MaintenanceTicketCreate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER, RoleEnum.ENGINEER, RoleEnum.EMPLOYEE]))
) -> Any:
    """
    Create new ticket.
    """
    item = maintenance_ticket.create(db, obj_in=item_in)
    return item

@router.put("/{id}", response_model=MaintenanceTicketResponse)
def update_ticket(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: MaintenanceTicketUpdate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER, RoleEnum.ENGINEER, RoleEnum.EMPLOYEE]))
) -> Any:
    """
    Update an existing ticket.
    """
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="MaintenanceTicket not found")
    item = maintenance_ticket.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/{id}", response_model=MaintenanceTicketResponse)
def read_ticket(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get ticket by ID.
    """
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="MaintenanceTicket not found")
    return item

@router.delete("/{id}", response_model=MaintenanceTicketResponse)
def delete_ticket(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER, RoleEnum.ENGINEER, RoleEnum.EMPLOYEE]))
) -> Any:
    """
    Delete a ticket.
    """
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="MaintenanceTicket not found")
    item = maintenance_ticket.remove(db, id=id)
    return item


from pydantic import BaseModel
class AssignRequest(BaseModel):
    engineer_id: UUID

class ResolveRequest(BaseModel):
    resolution_notes: str

@router.post("/{id}/assign", response_model=ActionResponse[MaintenanceTicketResponse])
def assign_ticket_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    assign_req: AssignRequest,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ActionResponse(success=True, message='Action successful', data=maintenance_ticket.assign(db, db_obj=item, engineer_id=assign_req.engineer_id))

@router.post("/{id}/start", response_model=ActionResponse[MaintenanceTicketResponse])
def start_ticket_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ActionResponse(success=True, message='Action successful', data=maintenance_ticket.start(db, db_obj=item))

@router.post("/{id}/resolve", response_model=ActionResponse[MaintenanceTicketResponse])
def resolve_ticket_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    resolve_req: ResolveRequest,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ActionResponse(success=True, message='Action successful', data=maintenance_ticket.resolve(db, db_obj=item, resolution_notes=resolve_req.resolution_notes))

@router.post("/{id}/close", response_model=ActionResponse[MaintenanceTicketResponse])
def close_ticket_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ActionResponse(success=True, message='Action successful', data=maintenance_ticket.close(db, db_obj=item))


WORKFLOW_ACTIONS = {
    "Open": ["assign"],
    "Assigned": ["start"],
    "In Progress": ["resolve"],
    "Resolved": ["close"],
    "Closed": []
}

@router.get("/{id}/workflow", response_model=WorkflowMetadataResponse)
def get_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    item = maintenance_ticket.get(db, id=id)
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
    return WorkflowHistoryService.get_history_for_entity(db, "tickets", str(id))

