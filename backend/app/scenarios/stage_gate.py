from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.scenarios.scenario_state_model import ScenarioState
from app.scenarios.scenario_manager import manager
from app.challenge_engine.transition import TransitionRules
from app.events.event_bus import EventBus
from app.events.events import StageAdvanced, ScenarioCompleted
from datetime import datetime, timezone

transition_checker = TransitionRules()

def get_in_progress_state(db: Session) -> Optional[ScenarioState]:
    return db.query(ScenarioState).filter(
        ScenarioState.status == "IN_PROGRESS"
    ).order_by(ScenarioState.started_at.desc()).first()

def find_stage(scenario: Dict[str, Any], stage_id: int) -> Optional[Dict[str, Any]]:
    if not scenario or "stages" not in scenario:
        return None
    for stage in scenario["stages"]:
        if stage.get("id") == stage_id:
            return stage
    return None

def get_active_stage(db: Session, target_endpoint: str) -> Optional[Dict[str, Any]]:
    state = get_in_progress_state(db)
    if not state:
        return None
    scenario = manager.registry.get_scenario(state.scenario_id)
    current = find_stage(scenario, state.current_stage)
    if current and current.get("target_endpoint") == target_endpoint:
        return current
    return None

def advance_if_stage_matches(db: Session, target_endpoint: str, action_context: Dict[str, Any], user_id: str = None):
    state = get_in_progress_state(db)
    if not state:
        # No active session for this user — do nothing. Learner must start a scenario first.
        return

    scenario = manager.registry.get_scenario(state.scenario_id)
    current = find_stage(scenario, state.current_stage)
    if not current or current.get("target_endpoint") != target_endpoint:
        return

    # Outcome-based check: pass scenario_id so transition rules are scenario-scoped
    if not transition_checker.check_transition(current, action_context, state.scenario_id):
        return

    # Advance stage
    completed = list(state.completed_stages) if state.completed_stages else []
    if current.get("id") not in completed:
        completed.append(current.get("id"))
    state.completed_stages = completed
    
    # Record timings
    meta = dict(state.metadata_json) if state.metadata_json else {}
    if "stage_completion_times" not in meta:
        meta["stage_completion_times"] = {}
    if "stage_start_times" not in meta:
        meta["stage_start_times"] = {}
        
    now_iso = datetime.now(timezone.utc).isoformat()
    meta["stage_completion_times"][str(state.current_stage)] = now_iso
    meta["stage_start_times"][str(state.current_stage + 1)] = now_iso
    state.metadata_json = meta
    
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(state, "metadata_json")

    state.current_stage += 1
    state.last_action = target_endpoint

    # Publish StageAdvanced
    EventBus.publish(StageAdvanced.create(
        entity_id=state.id,
        metadata={
            "scenario_id": state.scenario_id,
            "user_id": str(user_id),
            "stage_id": current.get("id"),
            "capability_gained": current.get("capability_gained"),
            "vulnerability_category": current.get("vulnerability_category"),
            "owasp": current.get("owasp"),
            "mitre": current.get("mitre"),
            "cvss": current.get("cvss")
        }
    ))

    # Wait for the user to explicitly end the session via frontend for final completion

    db.commit()
    db.refresh(state)
