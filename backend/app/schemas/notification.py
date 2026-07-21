from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.notification import NotificationSeverityEnum

class NotificationCreate(BaseModel):
    title: str
    message: str
    severity: NotificationSeverityEnum = NotificationSeverityEnum.INFO
    recipient_id: Optional[str] = None
    category: Optional[str] = None

class NotificationUpdate(BaseModel):
    read_status: bool

class NotificationResponse(NotificationCreate):
    id: UUID
    read_status: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
