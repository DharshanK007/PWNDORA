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
from typing import List, Optional
from datetime import date
from sqlalchemy import String, Date, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base


class FirmwareStatusEnum(str, enum.Enum):
    DRAFT = "Draft"
    PENDING_APPROVAL = "Pending Approval"
    APPROVED = "Approved"
    DEPLOYED = "Deployed"
    RETIRED = "Retired"

class Firmware(Base):
    __tablename__ = "firmwares"
    
    version_string: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    release_date: Mapped[date] = mapped_column(Date, nullable=False)
    file_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    s3_path: Mapped[str] = mapped_column(String(500), nullable=False)
    compatibility_matrix: Mapped[Optional[str]] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[FirmwareStatusEnum] = mapped_column(Enum(FirmwareStatusEnum), default=FirmwareStatusEnum.DRAFT, nullable=False)
    
    devices: Mapped[List["Device"]] = relationship(back_populates="firmware", lazy="selectin")
