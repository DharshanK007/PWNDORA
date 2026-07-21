from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, Dict
from datetime import datetime
from uuid import UUID

class AuditLogCreate(BaseModel):
    actor_user_id: Optional[str] = None
    target_entity: str
    target_entity_id: Optional[str] = None
    action: str
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    request_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    reason: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None

class AuditLogResponse(AuditLogCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
