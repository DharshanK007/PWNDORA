import os

os.makedirs("backend/app/scenarios", exist_ok=True)

# 1. Model
model_code = '''from sqlalchemy import String, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class Scenario(Base):
    __tablename__ = "scenarios"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    business_context: Mapped[str] = mapped_column(String(2000), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=True) # e.g. Beginner, Intermediate, Advanced
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    expected_learning_objectives: Mapped[list] = mapped_column(JSON, nullable=True)
    affected_assets: Mapped[list] = mapped_column(JSON, nullable=True)
'''
with open("backend/app/scenarios/scenario_model.py", "w") as f:
    f.write(model_code)

with open("backend/app/models/__init__.py", "a") as f:
    f.write("from app.scenarios.scenario_model import Scenario\n")

# 2. Schema
schema_code = '''from typing import Optional, List
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
'''
with open("backend/app/scenarios/scenario_schema.py", "w") as f:
    f.write(schema_code)

# 3. Service
service_code = '''from sqlalchemy.orm import Session
from app.scenarios.scenario_model import Scenario
from app.scenarios.scenario_schema import ScenarioCreate, ScenarioUpdate
from app.services.base import CRUDBase

class CRUDScenario(CRUDBase[Scenario, ScenarioCreate, ScenarioUpdate]):
    pass

scenario_service = CRUDScenario(Scenario)
'''
with open("backend/app/scenarios/scenario_service.py", "w") as f:
    f.write(service_code)

# 4. Router
router_code = '''from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.scenarios.scenario_schema import ScenarioResponse
from app.schemas.response import PaginatedResponse
from app.scenarios.scenario_service import scenario_service
from app.api.dependencies.query import QueryParameters, get_query_parameters

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
def read_scenarios(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters)
) -> Any:
    items, total = scenario_service.get_multi(db, params=params)
    return {
        "items": items,
        "pagination": {
            "skip": params.skip,
            "limit": params.limit,
            "total": total
        }
    }
'''
with open("backend/app/scenarios/scenario_router.py", "w") as f:
    f.write(router_code)

# Add to api.py
api_py = "backend/app/api/v1/api.py"
with open(api_py, "r") as f:
    api_content = f.read()

if "scenarios" not in api_content:
    api_content = api_content.replace("from app.api.v1.endpoints import (", "from app.scenarios import scenario_router\nfrom app.api.v1.endpoints import (")
    api_content += "\napi_router.include_router(scenario_router.router, prefix=\"/scenarios\", tags=[\"scenarios\"])\n"
    with open(api_py, "w") as f:
        f.write(api_content)

print("Phase 7 completed")
