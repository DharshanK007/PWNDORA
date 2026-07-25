content = '''from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api import deps
from app.core.config import settings
from app.events.event_bus import event_bus

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
        "event_bus": "initialized" if event_bus is not None else "missing"
    }

@router.get("/system/info")
def system_info():
    return {
        "project": settings.PROJECT_NAME,
        "ai_enabled": settings.ENABLE_AI,
        "attack_engine_enabled": settings.ENABLE_ATTACK_ENGINE,
        "replay_enabled": settings.ENABLE_REPLAY
    }
'''

with open("backend/app/api/v1/endpoints/health.py", "w") as f:
    f.write(content)

# Remove /health from main.py
filepath = "backend/app/main.py"
with open(filepath, "r") as f:
    content = f.read()
import re
content = re.sub(r'@app\.get\("/health"\)\s*def health_check\(\):\s*return \{.*?\}', '', content, flags=re.DOTALL)
with open(filepath, "w") as f:
    f.write(content)

# Add to api.py
api_filepath = "backend/app/api/v1/api.py"
with open(api_filepath, "r") as f:
    api_content = f.read()

if "health" not in api_content:
    api_content = api_content.replace("from app.api.v1.endpoints import (", "from app.api.v1.endpoints import (\n    health,")
    api_content = api_content + "\napi_router.include_router(health.router, prefix=\"/health\", tags=[\"health\"])\n"
    with open(api_filepath, "w") as f:
        f.write(api_content)
        
print("Added health endpoints")
