from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .network import NetworkZone
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
from sqlalchemy import String, ForeignKey, Enum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class DeviceStatusEnum(str, enum.Enum):
    NEW = "New"
    REGISTERED = "Registered"
    CONFIGURED = "Configured"
    ONLINE = "Online"
    MAINTENANCE = "Maintenance"
    OFFLINE = "Offline"
    DECOMMISSIONED = "Decommissioned"

class Device(Base):
    __tablename__ = "devices"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mac_address: Mapped[str] = mapped_column(String(17), unique=True, index=True, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    status: Mapped[DeviceStatusEnum] = mapped_column(Enum(DeviceStatusEnum), default=DeviceStatusEnum.OFFLINE, nullable=False)
    


    criticality_level: Mapped[Optional[str]] = mapped_column(String(50))
    operating_system: Mapped[Optional[str]] = mapped_column(String(100))
    last_patch_date: Mapped[Optional[str]] = mapped_column(String(50))
    maintenance_window: Mapped[Optional[str]] = mapped_column(String(100))
    communication_protocol: Mapped[Optional[str]] = mapped_column(String(100))
    vendor: Mapped[Optional[str]] = mapped_column(String(100))
    asset_group: Mapped[Optional[str]] = mapped_column(String(100))
    serial_number: Mapped[Optional[str]] = mapped_column(String(100))
    manufacturer: Mapped[Optional[str]] = mapped_column(String(100))
    warranty_expiry: Mapped[Optional[str]] = mapped_column(String(100)) # Simple date string
    lifecycle_status: Mapped[Optional[str]] = mapped_column(String(50), default="Active")
    assigned_engineer_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("employees.id"))
    network_zone_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("network_zones.id"))

    assigned_engineer: Mapped[Optional["Employee"]] = relationship("Employee", foreign_keys=[assigned_engineer_id], lazy="selectin")
    network_zone: Mapped[Optional["NetworkZone"]] = relationship("NetworkZone", back_populates="devices", lazy="selectin")

    location_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("machine_locations.id"))
    firmware_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("firmwares.id"))
    
    location: Mapped[Optional["MachineLocation"]] = relationship(back_populates="devices", lazy="selectin")
    firmware: Mapped[Optional["Firmware"]] = relationship(back_populates="devices", lazy="selectin")
    maintenance_tickets: Mapped[List["MaintenanceTicket"]] = relationship(back_populates="device", lazy="selectin")
