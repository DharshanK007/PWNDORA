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
from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base


class InventoryStatusEnum(str, enum.Enum):
    CREATED = "Created"
    AVAILABLE = "Available"
    ALLOCATED = "Allocated"
    CONSUMED = "Consumed"
    RESTOCKED = "Restocked"

class Inventory(Base):
    __tablename__ = "inventory"
    
    component_name: Mapped[str] = mapped_column(String(255), nullable=False)
    part_number: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    warehouse_zone: Mapped[Optional[str]] = mapped_column(String(100))
    supplier: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[InventoryStatusEnum] = mapped_column(Enum(InventoryStatusEnum), default=InventoryStatusEnum.CREATED, nullable=False)
