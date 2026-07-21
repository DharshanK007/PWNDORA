from app.schemas.response import ActionResponse
from app.api.dependencies.query import QueryParameters, get_query_parameters
from datetime import timedelta
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

@router.post("/login")
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    db_user = user.get_by_email(db, email=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        
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
