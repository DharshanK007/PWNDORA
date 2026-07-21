from sqlalchemy.orm import Session
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
