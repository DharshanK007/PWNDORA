from sqlalchemy import String, Boolean, DateTime, Text, JSON
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
