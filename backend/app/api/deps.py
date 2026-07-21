from typing import Generator, List, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal
from app.models import User, RoleEnum
from app.core.exceptions import UnauthorizedException, ForbiddenException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
        if token_data is None:
            raise UnauthorizedException(message="Could not validate credentials (no sub in token)")
    except (jwt.JWTError, ValidationError):
        raise UnauthorizedException(message="Could not validate credentials (jwt error)")
    
    user = db.query(User).filter(User.email == token_data).first()
    if not user:
        raise UnauthorizedException(message="User not found")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    # Right now all users are active, but this is a placeholder if we add is_active
    return current_user

class RoleChecker:
    def __init__(self, allowed_roles: List[RoleEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)) -> User:
        if user.role not in self.allowed_roles:
            raise ForbiddenException(message=f"Operation not permitted. Requires one of: {[r.name for r in self.allowed_roles]}")
        return user
