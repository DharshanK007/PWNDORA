from app.schemas.response import ActionResponse
from app.api.dependencies.query import QueryParameters, get_query_parameters
from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.schemas.user import UserResponse
from app.services import user

router = APIRouter()

# SE Stage 1: In-memory failed login tracker for the target helpdesk account
# Key: email, Value: list of datetime timestamps of failed attempts
_se_failed_attempts: dict[str, list] = {}

# The target account for Silent Exfiltration Stage 1
SE_TARGET_EMAIL = "jess.okafor@neofactory.com"
SE_BRUTE_FORCE_THRESHOLD = 5  # Minimum failed attempts before a success triggers Stage 1


@router.post("/login")
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    No rate-limiting exists on this endpoint — this is the real flaw for SE Stage 1.
    """
    db_user = user.get_by_email(db, email=form_data.username)

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        # Track failed attempt for SE Stage 1 target account
        if form_data.username == SE_TARGET_EMAIL:
            _se_failed_attempts.setdefault(form_data.username, []).append(datetime.utcnow())

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    # Successful login — check SE Stage 1 brute-force pattern
    if form_data.username == SE_TARGET_EMAIL:
        # Count failed attempts within the last 10 minutes
        window_start = datetime.utcnow() - timedelta(minutes=10)
        recent_fails = [
            t for t in _se_failed_attempts.get(form_data.username, [])
            if t > window_start
        ]
        if len(recent_fails) >= SE_BRUTE_FORCE_THRESHOLD:
            # Outcome-based: brute-force pattern confirmed — advance SE Stage 1
            from app.scenarios.stage_gate import advance_if_stage_matches
            advance_if_stage_matches(
                db,
                "POST /api/v1/auth/login",
                {"brute_force_pattern": True}
            )
        # Clear tracker after successful login regardless
        _se_failed_attempts.pop(form_data.username, None)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            subject=db_user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=UserResponse)
def test_token(
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Test access token.
    """
    return current_user
