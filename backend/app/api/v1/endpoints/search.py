from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Any, List
from app.api import deps
from app.models.user import User

class SearchRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/", response_model=dict)
def perform_global_search(
    req: SearchRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Global search endpoint.
    Vulnerable to injection when crafted queries are submitted.
    """
    from app.scenarios.stage_gate import advance_if_stage_matches
    
    # Fire stage gate check for Stage 3
    advance_if_stage_matches(db, str(current_user.id), "POST /api/v1/search", {"query": req.query})
    
    query_lower = req.query.lower()
    
    # If injection pattern or search term matches
    if any(term in query_lower for term in ["'", "or", "1=1", "%", "firmware", "select", "deploy", "log", "--", "union"]):
        results = [
            {
                "id": "log_sys_001",
                "title": "System Audit Log - Firmware Push Event",
                "category": "Deployment Logs",
                "snippet": "CRITICAL: Unauthorized firmware update pushed to Production Line 2 by session_user with overridden X-User-Role: Administrator in localStorage token.",
                "source": "syslog_sec_archive"
            },
            {
                "id": "log_sys_002",
                "title": "Production Line 2 Exception Log",
                "category": "System Logs",
                "snippet": "Line 2 halt triggered due to firmware checksum mismatch. Initiated by engineer account.",
                "source": "ot_mon_daemon"
            }
        ]
    else:
        results = [
            {
                "id": "res_001",
                "title": f"General Search Result for '{req.query}'",
                "category": "Documentation",
                "snippet": "No specific system anomalies found matching query.",
                "source": "kb_articles"
            }
        ]
        
    return {"query": req.query, "count": len(results), "items": results}
