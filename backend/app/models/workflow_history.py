from sqlalchemy import String, DateTime, Text, Integer
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
