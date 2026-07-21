from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.maintenance_ticket import PriorityEnum, TicketStatusEnum

class MaintenanceTicketBase(BaseModel):
    device_id: UUID
    assigned_to_id: Optional[UUID] = None
    created_by_id: UUID
    priority: PriorityEnum = PriorityEnum.MEDIUM
    status: TicketStatusEnum = TicketStatusEnum.OPEN
    issue_description: str = Field(..., min_length=10, max_length=2000)
    resolution_notes: Optional[str] = None

class MaintenanceTicketCreate(MaintenanceTicketBase):
    # Usually created_by_id is injected from the current user
    pass

class MaintenanceTicketUpdate(BaseModel):
    assigned_to_id: Optional[UUID] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[TicketStatusEnum] = None
    issue_description: Optional[str] = Field(None, min_length=10, max_length=2000)
    resolution_notes: Optional[str] = None

class MaintenanceTicketResponse(MaintenanceTicketBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
