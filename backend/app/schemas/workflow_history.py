from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class WorkflowHistoryCreate(BaseModel):
    entity: str
    entity_id: str
    old_state: Optional[str] = None
    new_state: str
    triggered_by: Optional[str] = None
    reason: Optional[str] = None
    transition_duration: Optional[int] = None
    transition_method: Optional[str] = None
    comments: Optional[str] = None

class WorkflowHistoryResponse(WorkflowHistoryCreate):
    id: UUID
    transition_time: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
