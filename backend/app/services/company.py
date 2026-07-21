from sqlalchemy.orm import Session
from app.models.company import CompanyProfile
from app.schemas.company import CompanyProfileCreate, CompanyProfileUpdate
from app.services.base import CRUDBase

class CRUDCompanyProfile(CRUDBase[CompanyProfile, CompanyProfileCreate, CompanyProfileUpdate]):
    def get_profile(self, db: Session) -> CompanyProfile:
        return db.query(self.model).first()

company = CRUDCompanyProfile(CompanyProfile)
