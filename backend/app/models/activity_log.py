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

from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    target_entity: Mapped[Optional[str]] = mapped_column(String(255))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    
    user: Mapped[Optional["User"]] = relationship(back_populates="activity_logs", lazy="selectin")
