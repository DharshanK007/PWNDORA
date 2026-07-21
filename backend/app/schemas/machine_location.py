from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class MachineLocationBase(BaseModel):
    factory_site: str
    zone: str
    description: Optional[str] = None

class MachineLocationCreate(MachineLocationBase):
    pass

class MachineLocationUpdate(BaseModel):
    factory_site: Optional[str] = None
    zone: Optional[str] = None
    description: Optional[str] = None

class MachineLocationResponse(MachineLocationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
