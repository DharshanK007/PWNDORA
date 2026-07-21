from sqlalchemy import String, Integer, JSON
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

    business_domain: Mapped[str] = mapped_column(String(100), nullable=True)
    security_level: Mapped[str] = mapped_column(String(100), nullable=True)
    factory_count: Mapped[int] = mapped_column(Integer, nullable=True)
    office_count: Mapped[int] = mapped_column(Integer, nullable=True)
    critical_infrastructure_type: Mapped[str] = mapped_column(String(100), nullable=True)
    timezone: Mapped[str] = mapped_column(String(100), nullable=True)
