from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
    from .department import Department
    from .employee import Employee
    from .machine_location import MachineLocation
    from .firmware import Firmware
    from .device import Device
    from .maintenance_ticket import MaintenanceTicket
    from .inventory import Inventory
    from .report import Report
    from .notification import Notification
    from .activity_log import ActivityLog

import enum
from typing import Optional
from sqlalchemy import String, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class PriorityEnum(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class TicketStatusEnum(str, enum.Enum):
    OPEN = "Open"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    UNDER_REVIEW = "Under Review"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    REJECTED = "Rejected"

class MaintenanceTicket(Base):
    __tablename__ = "maintenance_tickets"
    
    device_id: Mapped[str] = mapped_column(String(36), ForeignKey("devices.id"), nullable=False)
    assigned_to_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("employees.id"))
    created_by_id: Mapped[str] = mapped_column(String(36), ForeignKey("employees.id"), nullable=False)
    
    priority: Mapped[PriorityEnum] = mapped_column(Enum(PriorityEnum), default=PriorityEnum.LOW, nullable=False)
    status: Mapped[TicketStatusEnum] = mapped_column(Enum(TicketStatusEnum), default=TicketStatusEnum.OPEN, nullable=False)
    issue_description: Mapped[str] = mapped_column(Text, nullable=False)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    device: Mapped["Device"] = relationship(back_populates="maintenance_tickets", lazy="selectin")
    assigned_to: Mapped[Optional["Employee"]] = relationship(foreign_keys=[assigned_to_id], back_populates="maintenance_tickets_assigned", lazy="selectin")
    created_by: Mapped["Employee"] = relationship(foreign_keys=[created_by_id], back_populates="maintenance_tickets_created", lazy="selectin")
