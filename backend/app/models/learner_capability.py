from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.db.base_class import Base

class LearnerCapability(Base):
    __tablename__ = "learner_capabilities"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    capability: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_id: Mapped[str] = mapped_column(String(100), nullable=False)
    stage_id: Mapped[int] = mapped_column(nullable=False)
    earned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user: Mapped["User"] = relationship("User", lazy="selectin")
