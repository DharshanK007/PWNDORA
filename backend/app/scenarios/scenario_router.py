from typing import Any
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
    items = scenario_service.get_multi(db, params=params)
    total = scenario_service.get_count(db, params=params)
    return {
        "items": items,
        "pagination": {
            "skip": params.skip,
            "limit": params.limit,
            "total": total
        }
    }

from app.models.user import User
from app.scenarios.scenario_manager import manager

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
        ScenarioState.user_id == current_user.id
    ).order_by(ScenarioState.started_at.desc()).first()
    if not state:
        raise HTTPException(status_code=404, detail="State not found")
    return state

@router.get("/{scenario_id}/registry")
def get_scenario_registry(scenario_id: str):
    s = manager.registry.get_scenario(scenario_id)
    if not s:
        raise HTTPException(status_code=404, detail="Scenario definition not found")
    return s

