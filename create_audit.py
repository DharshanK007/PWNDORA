import os

base_dir = "backend/app/audit"
os.makedirs(base_dir, exist_ok=True)

# audit_models.py
with open(os.path.join(base_dir, "audit_models.py"), "w") as f:
    f.write('''from sqlalchemy import String, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    actor_user_id: Mapped[str] = mapped_column(String(36), nullable=True, index=True)
    target_entity: Mapped[str] = mapped_column(String(100), index=True)
    target_entity_id: Mapped[str] = mapped_column(String(36), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), index=True)
    previous_state: Mapped[str] = mapped_column(String(100), nullable=True)
    new_state: Mapped[str] = mapped_column(String(100), nullable=True)
    request_id: Mapped[str] = mapped_column(String(100), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, default=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=True) # Rich structured payload
''')

# audit_schema.py
with open(os.path.join(base_dir, "audit_schema.py"), "w") as f:
    f.write('''from pydantic import BaseModel, ConfigDict
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
''')

# audit_repository.py
with open(os.path.join(base_dir, "audit_repository.py"), "w") as f:
    f.write('''from sqlalchemy.orm import Session
from app.audit.audit_models import AuditLog
from app.audit.audit_schema import AuditLogCreate
from fastapi.encoders import jsonable_encoder

def create_audit_log(db: Session, obj_in: AuditLogCreate) -> AuditLog:
    obj_in_data = obj_in.model_dump()
    db_obj = AuditLog(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_audit_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

def get_audit_log(db: Session, id: str):
    return db.query(AuditLog).filter(AuditLog.id == id).first()
''')

# audit_service.py
with open(os.path.join(base_dir, "audit_service.py"), "w") as f:
    f.write('''from sqlalchemy.orm import Session
from app.audit.audit_schema import AuditLogCreate
from app.audit import audit_repository

class AuditService:
    @staticmethod
    def log_action(db: Session, log_data: AuditLogCreate):
        """
        Creates a new immutable audit log.
        """
        return audit_repository.create_audit_log(db, log_data)
        
    @staticmethod
    def get_logs(db: Session, skip: int = 0, limit: int = 100):
        return audit_repository.get_audit_logs(db, skip, limit)
        
    @staticmethod
    def get_log(db: Session, id: str):
        return audit_repository.get_audit_log(db, id)
''')

print("Created audit files.")
