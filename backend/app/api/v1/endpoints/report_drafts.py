from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.report import Report
from app.models.user import User
from app.scenarios.scenario_state_model import ScenarioState

router = APIRouter()

@router.get("/{scenario_state_id}")
def get_report_draft(
    scenario_state_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Returns the auto-generated draft report for the given scenario state.
    """
    # Verify ownership of the state
    state = db.query(ScenarioState).filter(
        ScenarioState.id == scenario_state_id,
        ScenarioState.user_id == current_user.id
    ).first()
    
    if not state:
        raise HTTPException(status_code=403, detail="Not authorized to access this scenario state")
        
    report = db.query(Report).filter(
        Report.scenario_state_id == scenario_state_id,
        Report.status == "Draft"
    ).first()
    
    if not report:
        from app.report_generator import generate_scenario_report
        report = generate_scenario_report(scenario_state_id, current_user.id)
        if not report:
            raise HTTPException(status_code=404, detail="No completed stages to generate a report")

        
    return {
        "id": report.id,
        "title": report.title,
        "content": report.summary, # Content stored in summary field
        "status": report.status.value
    }
