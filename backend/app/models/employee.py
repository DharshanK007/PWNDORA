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
from sqlalchemy import String, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class EmployeeStatusEnum(str, enum.Enum):
    PENDING = "Pending"
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    TERMINATED = "Terminated"

class Employee(Base):
    __tablename__ = "employees"
    
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    department_id: Mapped[str] = mapped_column(String(36), ForeignKey("departments.id"), nullable=False)
    
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[EmployeeStatusEnum] = mapped_column(Enum(EmployeeStatusEnum), default=EmployeeStatusEnum.PENDING, nullable=False)
    

    title: Mapped[Optional[str]] = mapped_column(String(100))
    shift: Mapped[Optional[str]] = mapped_column(String(50))
    office: Mapped[Optional[str]] = mapped_column(String(100))
    skills: Mapped[Optional[list]] = mapped_column(JSON)

    role_level: Mapped[Optional[str]] = mapped_column(String(50))
    hire_date: Mapped[Optional[str]] = mapped_column(String(50))
    last_login: Mapped[Optional[str]] = mapped_column(String(100))
    badge_id: Mapped[Optional[str]] = mapped_column(String(100))
    clearance_level: Mapped[Optional[str]] = mapped_column(String(50))
    employment_type: Mapped[Optional[str]] = mapped_column(String(50))
    workstation: Mapped[Optional[str]] = mapped_column(String(100))
    assigned_projects: Mapped[Optional[list]] = mapped_column(JSON)
    security_training_completed: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    manager_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("employees.id"))

    manager: Mapped[Optional["Employee"]] = relationship("Employee", remote_side="Employee.id", backref="direct_reports")
    user: Mapped["User"] = relationship(back_populates="employee", lazy="selectin")
    department: Mapped["Department"] = relationship(back_populates="employees", lazy="selectin")
    
    maintenance_tickets_assigned: Mapped[List["MaintenanceTicket"]] = relationship(foreign_keys="[MaintenanceTicket.assigned_to_id]", back_populates="assigned_to", lazy="selectin")
    maintenance_tickets_created: Mapped[List["MaintenanceTicket"]] = relationship(foreign_keys="[MaintenanceTicket.created_by_id]", back_populates="created_by", lazy="selectin")
    reports_generated: Mapped[List["Report"]] = relationship(back_populates="generated_by", lazy="selectin")
