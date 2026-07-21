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

from typing import List
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Department(Base):
    __tablename__ = "departments"
    
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    
    employees: Mapped[List["Employee"]] = relationship(back_populates="department", lazy="selectin")
