from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.report import ReportStatusEnum
from datetime import datetime
from uuid import UUID

class ReportBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    report_type: str
    file_path: str
    summary: Optional[str] = None
    status: Optional[ReportStatusEnum] = None
    generated_by_id: UUID
    status: ReportStatusEnum = ReportStatusEnum.DRAFT

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    summary: Optional[str] = None
    status: Optional[ReportStatusEnum] = None

class ReportResponse(ReportBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
