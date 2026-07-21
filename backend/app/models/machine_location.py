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

from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class MachineLocation(Base):
    __tablename__ = "machine_locations"
    
    factory_site: Mapped[str] = mapped_column(String(100), nullable=False)
    zone: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    
    devices: Mapped[List["Device"]] = relationship(back_populates="location", lazy="selectin")
