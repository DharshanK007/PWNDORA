import os

endpoints_dir = "backend/app/api/v1/endpoints"
os.makedirs(endpoints_dir, exist_ok=True)

routes = {
    "users": ("User", "UserCreate", "UserUpdate", "UserResponse", "user", "[RoleEnum.ADMINISTRATOR]"),
    "employees": ("Employee", "EmployeeCreate", "EmployeeUpdate", "EmployeeResponse", "employee", "[RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]"),
    "departments": ("Department", "DepartmentCreate", "DepartmentUpdate", "DepartmentResponse", "department", "[RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]"),
    "devices": ("Device", "DeviceCreate", "DeviceUpdate", "DeviceResponse", "device", "[RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]"),
    "firmwares": ("Firmware", "FirmwareCreate", "FirmwareUpdate", "FirmwareResponse", "firmware", "[RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]"),
    "locations": ("MachineLocation", "MachineLocationCreate", "MachineLocationUpdate", "MachineLocationResponse", "machine_location", "[RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]"),
    "tickets": ("MaintenanceTicket", "MaintenanceTicketCreate", "MaintenanceTicketUpdate", "MaintenanceTicketResponse", "maintenance_ticket", "[RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER, RoleEnum.ENGINEER, RoleEnum.EMPLOYEE]"),
    "inventory": ("Inventory", "InventoryCreate", "InventoryUpdate", "InventoryResponse", "inventory", "[RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]"),
    "notifications": ("Notification", "NotificationCreate", "NotificationUpdate", "NotificationResponse", "notification", "[RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER, RoleEnum.ENGINEER, RoleEnum.EMPLOYEE]"),
    "reports": ("Report", "ReportCreate", "ReportUpdate", "ReportResponse", "report", "[RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]"),
}

for name, (model, create_schema, update_schema, response_schema, svc, roles) in routes.items():
    content = f'''from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.models.user import RoleEnum
from app.schemas.base import PagedResponse
from app.schemas.{svc if name != "locations" and name != "tickets" else "machine_location" if name == "locations" else "maintenance_ticket"} import {create_schema}, {update_schema}, {response_schema}
from app.services import {svc}

router = APIRouter()

@router.get("/", response_model=PagedResponse[{response_schema}])
def read_{name}(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve {name}.
    """
    items = {svc}.get_multi(db, skip=skip, limit=limit)
    total = {svc}.get_count(db)
    return {{"items": items, "total": total, "skip": skip, "limit": limit}}

@router.post("/", response_model={response_schema}, status_code=status.HTTP_201_CREATED)
def create_{name[:-1]}(
    *,
    db: Session = Depends(deps.get_db),
    item_in: {create_schema},
    current_user = Depends(deps.RoleChecker({roles}))
) -> Any:
    """
    Create new {name[:-1]}.
    """
    item = {svc}.create(db, obj_in=item_in)
    return item

@router.put("/{{id}}", response_model={response_schema})
def update_{name[:-1]}(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: {update_schema},
    current_user = Depends(deps.RoleChecker({roles}))
) -> Any:
    """
    Update an existing {name[:-1]}.
    """
    item = {svc}.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="{model} not found")
    item = {svc}.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/{{id}}", response_model={response_schema})
def read_{name[:-1]}(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get {name[:-1]} by ID.
    """
    item = {svc}.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="{model} not found")
    return item

@router.delete("/{{id}}", response_model={response_schema})
def delete_{name[:-1]}(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker({roles}))
) -> Any:
    """
    Delete a {name[:-1]}.
    """
    item = {svc}.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="{model} not found")
    item = {svc}.remove(db, id=id)
    return item
'''
    with open(f"{endpoints_dir}/{name}.py", "w") as f:
        f.write(content)

# Activity Logs is read only
activity_content = '''from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import RoleEnum
from app.schemas.base import PagedResponse
from app.schemas.activity_log import ActivityLogResponse
from app.services import activity_log

router = APIRouter()

@router.get("/", response_model=PagedResponse[ActivityLogResponse])
def read_activity_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    items = activity_log.get_multi(db, skip=skip, limit=limit)
    total = activity_log.get_count(db)
    return {"items": items, "total": total, "skip": skip, "limit": limit}
'''
with open(f"{endpoints_dir}/activity_logs.py", "w") as f:
    f.write(activity_content)

