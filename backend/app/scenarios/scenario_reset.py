from sqlalchemy.orm import Session
from .scenario_state_model import ScenarioState
from .scenario_cache import ScenarioCache

class ScenarioReset:
    def __init__(self, cache: ScenarioCache):
        self.cache = cache

    def reset_scenario(self, db: Session, scenario_id: str, user_id: str):
        states = db.query(ScenarioState).filter(
            ScenarioState.scenario_id == scenario_id
        ).all()
        for state in states:
            state.status = "RESET"
        db.commit()
        
        self.cache.clear(scenario_id)
