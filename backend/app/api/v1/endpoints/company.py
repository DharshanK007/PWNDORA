from typing import Any
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
