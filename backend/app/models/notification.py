import enum
from sqlalchemy import String, Boolean, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
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
    recipient_id: Mapped[str] = mapped_column(String(36), ForeignKey('users.id'), index=True, nullable=True) # None = Broadcast
    read_status: Mapped[bool] = mapped_column(Boolean, default=False)
    category: Mapped[str] = mapped_column(String(100), nullable=True)

    recipient: Mapped[Optional['User']] = relationship(back_populates='notifications', lazy="selectin")
