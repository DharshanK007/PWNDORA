from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.get("/capabilities")
def get_capabilities(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Returns the accumulated capability graph for the current learner.
    """
    return {"capabilities": current_user.capabilities or {}}
