from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.scenarios.scenario_state_model import ScenarioState

router = APIRouter()

@router.get("/{scenario_id}")
def get_vulnerability_graph(
    scenario_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Returns the vulnerability graph for the user's latest session of this scenario.
    """
    state = db.query(ScenarioState).filter(
        ScenarioState.scenario_id == scenario_id,
        ScenarioState.user_id == current_user.id
    ).order_by(ScenarioState.started_at.desc()).first()
    
    if not state:
        raise HTTPException(status_code=404, detail="Scenario session not found")
        
    return {"vulnerability_graph": state.vulnerability_graph or []}
