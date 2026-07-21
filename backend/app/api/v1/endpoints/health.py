from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api import deps
from app.core.config import settings
from app.events.event_registry import registry

router = APIRouter()

@router.get("/")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

@router.get("/live")
def liveness_check():
    return {"status": "up"}

@router.get("/ready")
def readiness_check(db: Session = Depends(deps.get_db)):
    # Check DB connectivity
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "failed"
        
    return {
        "status": "ready" if db_status == "ok" else "not_ready",
        "database": db_status,
        "event_bus": "initialized" if registry is not None else "missing"
    }

@router.get("/system/info")
def system_info():
    return {
        "project": settings.PROJECT_NAME,
        "ai_enabled": settings.ENABLE_AI,
        "attack_engine_enabled": settings.ENABLE_ATTACK_ENGINE,
        "replay_enabled": settings.ENABLE_REPLAY
    }
