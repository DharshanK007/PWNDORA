import os

# 1. Model for NetworkZone
network_model = '''from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class NetworkZone(Base):
    __tablename__ = "network_zones"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    vlan_id: Mapped[int] = mapped_column(Integer, nullable=True)
    subnet: Mapped[str] = mapped_column(String(50), nullable=True)

    devices: Mapped[list["Device"]] = relationship("Device", back_populates="network_zone", lazy="selectin")
'''
with open("backend/app/models/network.py", "w") as f:
    f.write(network_model)

with open("backend/app/models/__init__.py", "a") as f:
    f.write("from .network import NetworkZone\n")

# 2. Schema for NetworkZone
network_schema = '''from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class NetworkZoneBase(BaseModel):
    name: str
    description: Optional[str] = None
    vlan_id: Optional[int] = None
    subnet: Optional[str] = None

class NetworkZoneCreate(NetworkZoneBase):
    pass

class NetworkZoneUpdate(NetworkZoneBase):
    pass

class NetworkZoneResponse(NetworkZoneBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
'''
with open("backend/app/schemas/network.py", "w") as f:
    f.write(network_schema)

# 3. Update Device Model
device_path = "backend/app/models/device.py"
with open(device_path, "r") as f:
    device_content = f.read()

device_fields = '''
    serial_number: Mapped[Optional[str]] = mapped_column(String(100))
    manufacturer: Mapped[Optional[str]] = mapped_column(String(100))
    warranty_expiry: Mapped[Optional[str]] = mapped_column(String(100)) # Simple date string
    lifecycle_status: Mapped[Optional[str]] = mapped_column(String(50), default="Active")
    assigned_engineer_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("employees.id"))
    network_zone_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("network_zones.id"))

    assigned_engineer: Mapped[Optional["Employee"]] = relationship("Employee", foreign_keys=[assigned_engineer_id], lazy="selectin")
    network_zone: Mapped[Optional["NetworkZone"]] = relationship("NetworkZone", back_populates="devices", lazy="selectin")
'''

if "serial_number" not in device_content:
    if "from sqlalchemy import String, ForeignKey, Enum" in device_content:
        device_content = device_content.replace("from sqlalchemy import String, ForeignKey, Enum", "from sqlalchemy import String, ForeignKey, Enum, Date")
    
    device_content = device_content.replace('    location_id: Mapped', device_fields + '\n    location_id: Mapped')
    
    # We also need to add NetworkZone to the type hinting block at the top if it's there
    if "from .network import NetworkZone" not in device_content:
        device_content = device_content.replace("from typing import TYPE_CHECKING", "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from .network import NetworkZone")

    with open(device_path, "w") as f:
        f.write(device_content)

# 4. Update Device Schema
device_schema_path = "backend/app/schemas/device.py"
with open(device_schema_path, "r") as f:
    device_schema = f.read()

device_schema_fields = '''
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    warranty_expiry: Optional[str] = None
    lifecycle_status: Optional[str] = None
    assigned_engineer_id: Optional[UUID] = None
    network_zone_id: Optional[UUID] = None
'''

if "serial_number" not in device_schema:
    device_schema = device_schema.replace('    status: Optional', device_schema_fields + '    status: Optional')
    
    # For Update
    device_schema = device_schema.replace('    mac_address: Optional', device_schema_fields + '    mac_address: Optional')
    
    with open(device_schema_path, "w") as f:
        f.write(device_schema)

print("Phase 4 & 5 updated")
