from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class CompanyProfileBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    headquarters: Optional[str] = None
    business_units: Optional[List[str]] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    contact_email: Optional[str] = None
    business_domain: Optional[str] = None
    security_level: Optional[str] = None
    factory_count: Optional[int] = None
    office_count: Optional[int] = None
    critical_infrastructure_type: Optional[str] = None
    timezone: Optional[str] = None


class CompanyProfileCreate(CompanyProfileBase):
    pass

class CompanyProfileUpdate(CompanyProfileBase):
    pass

class CompanyProfileResponse(CompanyProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
