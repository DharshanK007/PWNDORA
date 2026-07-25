import os

ep_content = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.scenarios.scenario_manager import manager
from app.vulnerabilities.authentication.endpoints import router as auth_vuln_router

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
        ScenarioState.user_id == current_user.id
    ).order_by(ScenarioState.started_at.desc()).first()
    if not state:
        raise HTTPException(status_code=404, detail="State not found")
    return state

# Dynamic mount for vulnerabilities
vulnerable_router = APIRouter()
vulnerable_router.include_router(auth_vuln_router, prefix="/auth")

@router.api_route("/{scenario_id}/vulnerable/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
def route_vulnerable(scenario_id: str, path: str, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    from app.scenarios.scenario_state_model import ScenarioState
    state = db.query(ScenarioState).filter(
        ScenarioState.scenario_id == scenario_id,
        ScenarioState.user_id == current_user.id,
        ScenarioState.status == "IN_PROGRESS"
    ).first()
    if not state:
        raise HTTPException(status_code=403, detail="Scenario not active")
    # In a real dynamic setup we would dispatch this to the vulnerable_router internally
    # For now, simply return a mock vulnerable response if auth is hit
    if path == "auth/login":
        return {"token": "scenario_admin_token", "message": "Vulnerable Login hit!"}
    raise HTTPException(status_code=404, detail="Vulnerable route not found")
'''
with open("backend/app/api/v1/endpoints/scenarios.py", "w") as f: f.write(ep_content)

# Update api.py
api_path = "backend/app/api/v1/api.py"
with open(api_path, "r") as f: api_content = f.read()

if "scenarios.router" not in api_content:
    api_content = api_content.replace(
        "from app.api.v1.endpoints import (",
        "from app.api.v1.endpoints import (\n    scenarios,"
    )
    api_content += '\napi_router.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])\n'
    with open(api_path, "w") as f: f.write(api_content)

print("Created scenarios router")
