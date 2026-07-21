from sqlalchemy.orm import Session
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
