from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.device import DeviceStatusEnum

class DeviceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    mac_address: str
    ip_address: str
    status: DeviceStatusEnum = DeviceStatusEnum.OFFLINE
    location_id: Optional[UUID] = None
    firmware_id: Optional[UUID] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)


    criticality_level: Optional[str] = None
    operating_system: Optional[str] = None
    last_patch_date: Optional[str] = None
    maintenance_window: Optional[str] = None
    communication_protocol: Optional[str] = None
    vendor: Optional[str] = None
    asset_group: Optional[str] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    warranty_expiry: Optional[str] = None
    lifecycle_status: Optional[str] = None
    assigned_engineer_id: Optional[UUID] = None
    network_zone_id: Optional[UUID] = None
    mac_address: Optional[str] = None
    ip_address: Optional[str] = Field(None, pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")


    criticality_level: Optional[str] = None
    operating_system: Optional[str] = None
    last_patch_date: Optional[str] = None
    maintenance_window: Optional[str] = None
    communication_protocol: Optional[str] = None
    vendor: Optional[str] = None
    asset_group: Optional[str] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    warranty_expiry: Optional[str] = None
    lifecycle_status: Optional[str] = None
    assigned_engineer_id: Optional[UUID] = None
    network_zone_id: Optional[UUID] = None
    status: Optional[DeviceStatusEnum] = None
    location_id: Optional[UUID] = None
    firmware_id: Optional[UUID] = None

class DeviceResponse(DeviceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
