from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.firmware import FirmwareStatusEnum
from datetime import datetime, date
from uuid import UUID

class FirmwareBase(BaseModel):
    version_string: str
    release_date: date
    file_hash: str
    s3_path: str
    compatibility_matrix: str
    is_active: bool = False
    status: FirmwareStatusEnum = FirmwareStatusEnum.DRAFT

class FirmwareCreate(FirmwareBase):
    pass

class FirmwareUpdate(BaseModel):
    version_string: Optional[str] = None
    release_date: Optional[date] = None
    file_hash: Optional[str] = None
    s3_path: Optional[str] = None
    compatibility_matrix: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[FirmwareStatusEnum] = None

class FirmwareResponse(FirmwareBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
