from sqlalchemy import String, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Scenario(Base):
    __tablename__ = "scenarios"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    business_context: Mapped[str] = mapped_column(String(2000), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=True) # e.g. Beginner, Intermediate, Advanced
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    expected_learning_objectives: Mapped[list] = mapped_column(JSON, nullable=True)

    scenario_type: Mapped[str] = mapped_column(String(100), nullable=True)
    business_impact: Mapped[str] = mapped_column(String(100), nullable=True)
    target_department_id: Mapped[str] = mapped_column(String(36), ForeignKey("departments.id"), nullable=True)
    estimated_duration: Mapped[str] = mapped_column(String(100), nullable=True)
    required_roles: Mapped[list] = mapped_column(JSON, nullable=True)
    tags: Mapped[list] = mapped_column(JSON, nullable=True)
    affected_assets: Mapped[list] = mapped_column(JSON, nullable=True)

    states: Mapped[list["ScenarioState"]] = relationship("ScenarioState", back_populates="scenario", cascade="all, delete-orphan")
