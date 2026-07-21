from pydantic import BaseModel, Field, EmailStr, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    role: RoleEnum = RoleEnum.EMPLOYEE

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
