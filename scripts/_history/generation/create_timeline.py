import os

with open("backend/app/api/v1/endpoints/timeline.py", "w") as f:
    f.write('''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from typing import Any, List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel
from app.audit.audit_models import AuditLog
from app.models.workflow_history import WorkflowHistory
from sqlalchemy import desc

router = APIRouter()

class TimelineEventResponse(BaseModel):
    event_id: str
    event_type: str
    entity: str
    entity_id: Optional[str] = None
    action: str
    actor_user_id: Optional[str] = None
    timestamp: datetime
    details: Dict[str, Any] = {}

@router.get("/", response_model=List[TimelineEventResponse])
def get_timeline(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(deps.get_current_user)
) -> Any:
    \"\"\"
    Retrieve a unified chronological system timeline.
    \"\"\"
    audit_logs = db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit).all()
    history_logs = db.query(WorkflowHistory).order_by(desc(WorkflowHistory.transition_time)).limit(limit).all()
    
    events = []
    for a in audit_logs:
        events.append(TimelineEventResponse(
            event_id=a.id,
            event_type="audit",
            entity=a.target_entity,
            entity_id=a.target_entity_id,
            action=a.action,
            actor_user_id=a.actor_user_id,
            timestamp=a.created_at,
            details={"previous_state": a.previous_state, "new_state": a.new_state}
        ))
        
    for h in history_logs:
        events.append(TimelineEventResponse(
            event_id=h.id,
            event_type="history",
            entity=h.entity,
            entity_id=h.entity_id,
            action=h.transition_method or "transition",
            actor_user_id=h.triggered_by,
            timestamp=h.transition_time,
            details={"old_state": h.old_state, "new_state": h.new_state}
        ))
        
    events.sort(key=lambda x: x.timestamp, reverse=True)
    return events[skip:skip+limit]
''')

# Add to api router
api_file = "backend/app/api/v1/api.py"
with open(api_file, "r") as f:
    content = f.read()

if "from app.api.v1.endpoints import timeline" not in content:
    content = content.replace(
        "from app.api.v1.endpoints import audit", 
        "from app.api.v1.endpoints import audit\nfrom app.api.v1.endpoints import timeline"
    )
    content += '\napi_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])\n'
    with open(api_file, "w") as f:
        f.write(content)

print("Created Timeline endpoint.")
