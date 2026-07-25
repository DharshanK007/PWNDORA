import os

router_path = "backend/app/scenarios/scenario_router.py"

append = '''
from app.models.user import User
from app.scenarios.scenario_manager import manager
from app.vulnerabilities.authentication.endpoints import router as auth_vuln_router

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

# Dynamic Vulnerability endpoints
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
    
    if path == "auth/login":
        return {"token": "scenario_admin_token", "message": "Vulnerable Login hit!"}
    raise HTTPException(status_code=404, detail="Vulnerable route not found")
'''
with open(router_path, "a") as f: f.write(append)
print("Merged API routes")
