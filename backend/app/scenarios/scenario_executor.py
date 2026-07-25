from sqlalchemy.orm import Session
from .scenario_state_model import ScenarioState
from datetime import datetime, timezone
import uuid

class ScenarioExecutor:
    def start_scenario(self, db: Session, scenario_id: str, user_id: str) -> ScenarioState:
        # Check if already running
        existing = db.query(ScenarioState).filter(
            ScenarioState.scenario_id == scenario_id,
            ScenarioState.user_id == user_id,
            ScenarioState.status == "IN_PROGRESS"
        ).first()
        if existing:
            return existing
            
        state = ScenarioState(
            scenario_id=scenario_id,
            user_id=user_id,
            status="IN_PROGRESS",
            current_stage=1,
            started_at=datetime.now(timezone.utc),
            metadata_json={
                "stage_start_times": {"1": datetime.now(timezone.utc).isoformat()},
                "stage_completion_times": {},
                "answers": {}
            }
        )
        db.add(state)
        db.commit()
        db.refresh(state)
        return state
