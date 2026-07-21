from sqlalchemy.orm import Session
from app.scenarios.scenario_model import Scenario
from app.scenarios.scenario_schema import ScenarioCreate, ScenarioUpdate
from app.services.base import CRUDBase

class CRUDScenario(CRUDBase[Scenario, ScenarioCreate, ScenarioUpdate]):
    pass

scenario_service = CRUDScenario(Scenario)
