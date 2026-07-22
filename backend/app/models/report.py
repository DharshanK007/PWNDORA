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
from sqlalchemy import String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.scenarios.scenario_state_model import ScenarioState

class ReportStatusEnum(str, enum.Enum):
    DRAFT = "Draft"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"

class Report(Base):
    __tablename__ = "reports"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    report_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[ReportStatusEnum] = mapped_column(Enum(ReportStatusEnum), default=ReportStatusEnum.DRAFT, nullable=False)
    
    generated_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("employees.id"))
    scenario_state_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("scenario_states.id"), nullable=True)
    
    generated_by: Mapped[Optional["Employee"]] = relationship(back_populates="reports_generated", lazy="selectin")
    scenario_state: Mapped[Optional["ScenarioState"]] = relationship(lazy="selectin")
