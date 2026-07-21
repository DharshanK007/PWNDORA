from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class NetworkZoneBase(BaseModel):
    name: str
    description: Optional[str] = None
    trust_level: Optional[str] = None
    routing_direction: Optional[str] = None

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

class NetworkLinkBase(BaseModel):
    source_zone_id: UUID
    target_zone_id: UUID
    description: Optional[str] = None
    trust_level: Optional[str] = None
    routing_direction: Optional[str] = None


class NetworkLinkCreate(NetworkLinkBase):
    pass

class NetworkLinkUpdate(NetworkLinkBase):
    pass

class NetworkLinkResponse(NetworkLinkBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
