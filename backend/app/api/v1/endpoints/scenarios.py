from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.scenarios.scenario_manager import manager
from datetime import datetime, timezone

from pydantic import BaseModel

class ActionRequest(BaseModel):
    action: str

router = APIRouter()

@router.get("/")
def list_scenarios():
    return manager.registry.list_scenarios()

@router.get("/{scenario_id}")
def get_scenario(scenario_id: str):
    s = manager.registry.get_scenario(scenario_id)
    if not s:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return s

@router.post("/{scenario_id}/start")
def start_scenario(scenario_id: str, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    state = manager.start(db, scenario_id, current_user.id)
    return {"status": "started", "state": state}

@router.post("/{scenario_id}/reset")
def reset_scenario(scenario_id: str, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    manager.reset(db, scenario_id, current_user.id)
    return {"status": "reset"}

@router.get("/{scenario_id}/state")
def get_scenario_state(scenario_id: str, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    from app.scenarios.scenario_state_model import ScenarioState
    state = db.query(ScenarioState).filter(
        ScenarioState.scenario_id == scenario_id,
        ScenarioState.user_id == str(current_user.id)
    ).order_by(ScenarioState.started_at.desc()).first()
    if not state:
        state = manager.start(db, scenario_id, str(current_user.id))
    return state

@router.post("/{scenario_id}/action")
def perform_action(scenario_id: str, req: ActionRequest, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    from app.scenarios.scenario_state_model import ScenarioState
    from app.events.event_bus import EventBus
    from app.events.events import StageAdvanced, ScenarioCompleted
    
    state = db.query(ScenarioState).filter(
        ScenarioState.scenario_id == scenario_id,
        ScenarioState.user_id == current_user.id
    ).order_by(ScenarioState.started_at.desc()).first()
    
    if not state or state.status != "IN_PROGRESS":
        raise HTTPException(status_code=400, detail="Scenario not in progress")
        
    scenario = manager.registry.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    if req.action == "end_session":
        state.status = "COMPLETED"
        state.completed_at = datetime.now(timezone.utc)
        EventBus.publish(ScenarioCompleted.create(
            entity_id=state.id,
            metadata={
                "scenario_id": scenario_id,
                "user_id": str(current_user.id),
                "score": len(state.completed_stages) * 25 if state.completed_stages else 0
            }
        ))
        db.commit()
        db.refresh(state)
        return {"status": "success", "state": state}

        
    stages = scenario.get("stages", [])
    current_stage_idx = state.current_stage - 1
    if current_stage_idx < len(stages):
        current_stage = stages[current_stage_idx]
        if current_stage.get("required_action") == req.action:
            # Mark complete
            completed = list(state.completed_stages) if state.completed_stages else []
            if current_stage.get("id") not in completed:
                completed.append(current_stage.get("id"))
            state.completed_stages = completed
            state.current_stage += 1
            
            # Fire event
            EventBus.publish(StageAdvanced.create(
                entity_id=state.id,
                metadata={
                    "scenario_id": scenario_id,
                    "user_id": str(current_user.id),
                    "stage_id": current_stage.get("id"),
                    "capability_gained": current_stage.get("capability_gained"),
                    "vulnerability_category": current_stage.get("vulnerability_category")
                }
            ))
            
            # Check if finished
            if state.current_stage > len(stages):
                state.status = "COMPLETED"
                state.completed_at = datetime.now(timezone.utc)
                EventBus.publish(ScenarioCompleted.create(
                    entity_id=state.id,
                    metadata={
                        "scenario_id": scenario_id,
                        "user_id": str(current_user.id),
                        "score": 100
                    }
                ))
            
            db.commit()
            db.refresh(state)
            
    return {"status": "success", "state": state}

