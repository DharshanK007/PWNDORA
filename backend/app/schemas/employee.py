from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.employee import EmployeeStatusEnum
from datetime import datetime
from uuid import UUID

class EmployeeBase(BaseModel):
    user_id: UUID
    department_id: UUID
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)

    title: Optional[str] = None
    shift: Optional[str] = None
    office: Optional[str] = None
    skills: Optional[list] = None

    role_level: Optional[str] = None
    hire_date: Optional[str] = None
    last_login: Optional[str] = None
    badge_id: Optional[str] = None
    clearance_level: Optional[str] = None
    employment_type: Optional[str] = None
    workstation: Optional[str] = None
    assigned_projects: Optional[list] = None
    security_training_completed: Optional[bool] = None
    manager_id: Optional[UUID] = None

    title: Optional[str] = None
    shift: Optional[str] = None
    office: Optional[str] = None
    skills: Optional[list] = None

    role_level: Optional[str] = None
    hire_date: Optional[str] = None
    last_login: Optional[str] = None
    badge_id: Optional[str] = None
    clearance_level: Optional[str] = None
    employment_type: Optional[str] = None
    workstation: Optional[str] = None
    assigned_projects: Optional[list] = None
    security_training_completed: Optional[bool] = None
    manager_id: Optional[UUID] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    status: Optional[EmployeeStatusEnum] = None
    status: EmployeeStatusEnum = EmployeeStatusEnum.PENDING

class EmployeeCreate(EmployeeBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "department_id": "123e4567-e89b-12d3-a456-426614174001",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+1234567890",
                "status": "Pending"
            }
        }
    )


class EmployeeUpdate(BaseModel):
    department_id: Optional[UUID] = None

    title: Optional[str] = None
    shift: Optional[str] = None
    office: Optional[str] = None
    skills: Optional[list] = None

    role_level: Optional[str] = None
    hire_date: Optional[str] = None
    last_login: Optional[str] = None
    badge_id: Optional[str] = None
    clearance_level: Optional[str] = None
    employment_type: Optional[str] = None
    workstation: Optional[str] = None
    assigned_projects: Optional[list] = None
    security_training_completed: Optional[bool] = None
    manager_id: Optional[UUID] = None
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)

    title: Optional[str] = None
    shift: Optional[str] = None
    office: Optional[str] = None
    skills: Optional[list] = None

    role_level: Optional[str] = None
    hire_date: Optional[str] = None
    last_login: Optional[str] = None
    badge_id: Optional[str] = None
    clearance_level: Optional[str] = None
    employment_type: Optional[str] = None
    workstation: Optional[str] = None
    assigned_projects: Optional[list] = None
    security_training_completed: Optional[bool] = None
    manager_id: Optional[UUID] = None

    title: Optional[str] = None
    shift: Optional[str] = None
    office: Optional[str] = None
    skills: Optional[list] = None

    role_level: Optional[str] = None
    hire_date: Optional[str] = None
    last_login: Optional[str] = None
    badge_id: Optional[str] = None
    clearance_level: Optional[str] = None
    employment_type: Optional[str] = None
    workstation: Optional[str] = None
    assigned_projects: Optional[list] = None
    security_training_completed: Optional[bool] = None
    manager_id: Optional[UUID] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    status: Optional[EmployeeStatusEnum] = None
    status: EmployeeStatusEnum = EmployeeStatusEnum.PENDING

class EmployeeResponse(EmployeeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
