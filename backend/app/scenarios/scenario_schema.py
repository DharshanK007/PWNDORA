from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class ScenarioBase(BaseModel):
    title: str
    description: Optional[str] = None
    business_context: Optional[str] = None
    difficulty: Optional[str] = None
    category: Optional[str] = None
    expected_learning_objectives: Optional[List[str]] = None

    scenario_type: Optional[str] = None
    business_impact: Optional[str] = None
    target_department_id: Optional[UUID] = None
    estimated_duration: Optional[str] = None
    required_roles: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    affected_assets: Optional[List[str]] = None

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioUpdate(ScenarioBase):
    pass

class ScenarioResponse(ScenarioBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
