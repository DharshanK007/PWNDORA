import os

# app/models/notification.py
with open("backend/app/models/notification.py", "w") as f:
    f.write('''import enum
from sqlalchemy import String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class NotificationSeverityEnum(str, enum.Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Notification(Base):
    __tablename__ = "notifications"

    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    severity: Mapped[NotificationSeverityEnum] = mapped_column(Enum(NotificationSeverityEnum), default=NotificationSeverityEnum.INFO)
    recipient_id: Mapped[str] = mapped_column(String(36), index=True, nullable=True) # None = Broadcast
    read_status: Mapped[bool] = mapped_column(Boolean, default=False)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
''')

# app/models/workflow_history.py
with open("backend/app/models/workflow_history.py", "w") as f:
    f.write('''from sqlalchemy import String, DateTime, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
from datetime import datetime, timezone

class WorkflowHistory(Base):
    __tablename__ = "workflow_history"

    entity: Mapped[str] = mapped_column(String(100), index=True)
    entity_id: Mapped[str] = mapped_column(String(36), index=True)
    old_state: Mapped[str] = mapped_column(String(100), nullable=True)
    new_state: Mapped[str] = mapped_column(String(100))
    transition_time: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    triggered_by: Mapped[str] = mapped_column(String(36), nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    transition_duration: Mapped[int] = mapped_column(Integer, nullable=True) # in seconds
    transition_method: Mapped[str] = mapped_column(String(100), nullable=True)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
''')

# app/schemas/notification.py
with open("backend/app/schemas/notification.py", "w") as f:
    f.write('''from pydantic import BaseModel, ConfigDict
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
''')

# app/schemas/workflow_history.py
with open("backend/app/schemas/workflow_history.py", "w") as f:
    f.write('''from pydantic import BaseModel, ConfigDict
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
''')

# app/services/notification.py
with open("backend/app/services/notification.py", "w") as f:
    f.write('''from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate
from app.services.base import CRUDBase

class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    def mark_read(self, db: Session, *, db_obj: Notification) -> Notification:
        db_obj.read_status = True
        db.commit()
        db.refresh(db_obj)
        return db_obj

NotificationService = CRUDNotification(Notification)
''')

# app/services/workflow_history.py
with open("backend/app/services/workflow_history.py", "w") as f:
    f.write('''from sqlalchemy.orm import Session
from app.models.workflow_history import WorkflowHistory
from app.schemas.workflow_history import WorkflowHistoryCreate
from typing import List

class WorkflowHistoryService:
    @staticmethod
    def record_transition(db: Session, obj_in: WorkflowHistoryCreate) -> WorkflowHistory:
        obj_in_data = obj_in.model_dump()
        db_obj = WorkflowHistory(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    @staticmethod
    def get_history_for_entity(db: Session, entity: str, entity_id: str) -> List[WorkflowHistory]:
        return db.query(WorkflowHistory).filter(
            WorkflowHistory.entity == entity,
            WorkflowHistory.entity_id == entity_id
        ).order_by(WorkflowHistory.transition_time.desc()).all()
''')

# app/api/v1/endpoints/notifications.py
with open("backend/app/api/v1/endpoints/notifications.py", "w") as f:
    f.write('''from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.services.notification import NotificationService
from app.schemas.notification import NotificationResponse, NotificationUpdate
from app.schemas.base import PagedResponse
from app.models.user import RoleEnum

router = APIRouter()

@router.get("/", response_model=PagedResponse[NotificationResponse])
def read_notifications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve notifications for current user.
    """
    items = db.query(NotificationService.model).filter(
        NotificationService.model.recipient_id == str(current_user.id)
    ).offset(skip).limit(limit).all()
    
    total = db.query(NotificationService.model).filter(
        NotificationService.model.recipient_id == str(current_user.id)
    ).count()
    return {"items": items, "total": total, "skip": skip, "limit": limit}

@router.patch("/{id}/read", response_model=NotificationResponse)
def mark_notification_read(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Mark a notification as read.
    """
    item = NotificationService.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Notification not found")
    if item.recipient_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return NotificationService.mark_read(db, db_obj=item)
''')

print("Created notification and history files.")
