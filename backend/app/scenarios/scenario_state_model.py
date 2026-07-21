from typing import Optional, Any
from sqlalchemy import String, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.db.base_class import Base

class ScenarioState(Base):
    __tablename__ = "scenario_states"

    scenario_id: Mapped[str] = mapped_column(String(36), ForeignKey("scenarios.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    current_stage: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    current_objective: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="IN_PROGRESS", nullable=False) # e.g. IN_PROGRESS, COMPLETED, RESET
    
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_action: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_resource_opened: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_checkpoint: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    metadata_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)

    scenario = relationship("Scenario", back_populates="states")
    user = relationship("User", back_populates="scenario_states")
