import os

os.makedirs("backend/app/models", exist_ok=True)
os.makedirs("backend/app/schemas", exist_ok=True)
os.makedirs("backend/app/services", exist_ok=True)

# 1. Model
model_code = '''from sqlalchemy import String, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class CompanyProfile(Base):
    __tablename__ = "company_profiles"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_url: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    headquarters: Mapped[str] = mapped_column(String(255), nullable=True)
    business_units: Mapped[list] = mapped_column(JSON, nullable=True)
    industry: Mapped[str] = mapped_column(String(100), nullable=True)
    employee_count: Mapped[int] = mapped_column(Integer, nullable=True)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=True)
'''
with open("backend/app/models/company.py", "w") as f:
    f.write(model_code)

# 2. Schema
schema_code = '''from typing import Optional, List
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

class CompanyProfileCreate(CompanyProfileBase):
    pass

class CompanyProfileUpdate(CompanyProfileBase):
    pass

class CompanyProfileResponse(CompanyProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
'''
with open("backend/app/schemas/company.py", "w") as f:
    f.write(schema_code)

# 3. Service
service_code = '''from sqlalchemy.orm import Session
from app.models.company import CompanyProfile
from app.schemas.company import CompanyProfileCreate, CompanyProfileUpdate
from app.services.base import CRUDBase

class CRUDCompanyProfile(CRUDBase[CompanyProfile, CompanyProfileCreate, CompanyProfileUpdate]):
    def get_profile(self, db: Session) -> CompanyProfile:
        return db.query(self.model).first()

company = CRUDCompanyProfile(CompanyProfile)
'''
with open("backend/app/services/company.py", "w") as f:
    f.write(service_code)

# 4. Router
router_code = '''from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.company import CompanyProfileResponse
from app.schemas.response import ActionResponse
from app.services.company import company

router = APIRouter()

@router.get("/", response_model=CompanyProfileResponse)
def read_company_profile(
    db: Session = Depends(deps.get_db)
) -> Any:
    profile = company.get_profile(db)
    if not profile:
        raise HTTPException(status_code=404, detail="Company profile not found")
    return profile
'''
with open("backend/app/api/v1/endpoints/company.py", "w") as f:
    f.write(router_code)

# 5. Add to __init__.py and api.py
with open("backend/app/models/__init__.py", "a") as f:
    f.write("from .company import CompanyProfile\n")

with open("backend/app/services/__init__.py", "a") as f:
    f.write("from .company import company\n")

api_py = "backend/app/api/v1/api.py"
with open(api_py, "r") as f:
    api_content = f.read()

if "endpoints.company" not in api_content and "company" not in api_content:
    api_content = api_content.replace("from app.api.v1.endpoints import (", "from app.api.v1.endpoints import (\n    company,")
    api_content += "\napi_router.include_router(company.router, prefix=\"/company\", tags=[\"company\"])\n"
    with open(api_py, "w") as f:
        f.write(api_content)

print("Phase 1 completed")
