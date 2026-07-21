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
from typing import Optional, List
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class RoleEnum(str, enum.Enum):
    EMPLOYEE = "Employee"
    ENGINEER = "Engineer"
    MANAGER = "Manager"
    ADMINISTRATOR = "Administrator"

class User(Base):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.EMPLOYEE, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    employee: Mapped[Optional["Employee"]] = relationship(back_populates="user", uselist=False, lazy="selectin")
    activity_logs: Mapped[List["ActivityLog"]] = relationship(back_populates="user", lazy="selectin")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="recipient", foreign_keys='Notification.recipient_id', lazy="selectin")
    scenario_states: Mapped[list["ScenarioState"]] = relationship("ScenarioState", back_populates="user", cascade="all, delete-orphan")
