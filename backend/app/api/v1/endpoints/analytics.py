from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.scenarios.scenario_state_model import ScenarioState
from typing import List

router = APIRouter()

@router.get("/live-sessions")
def get_live_sessions(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RoleChecker([deps.RoleEnum.ADMINISTRATOR, deps.RoleEnum.MANAGER]))
):
    """
    Admin-only endpoint to view all active cyber range sessions.
    """
    active_states = db.query(ScenarioState).filter(
        ScenarioState.status == "IN_PROGRESS"
    ).all()
    
    result = []
    for state in active_states:
        user = state.user
        result.append({
            "id": state.id,
            "scenario_id": state.scenario_id,
            "user_email": user.email if user else "Unknown",
            "current_stage": state.current_stage,
            "started_at": state.started_at,
            "attempts": state.attempts
        })
        
    return {"sessions": result}
