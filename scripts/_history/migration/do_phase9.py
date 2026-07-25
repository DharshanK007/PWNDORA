import os

dashboard_code = '''from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.models.device import Device, DeviceStatusEnum
from app.models.employee import Employee, EmployeeStatusEnum
from app.models.maintenance_ticket import MaintenanceTicket, TicketStatusEnum

router = APIRouter()

@router.get("/summary")
def get_summary(db: Session = Depends(deps.get_db)) -> Any:
    total_assets = db.query(func.count(Device.id)).scalar()
    online_assets = db.query(func.count(Device.id)).filter(Device.status == DeviceStatusEnum.ONLINE).scalar()
    
    total_employees = db.query(func.count(Employee.id)).scalar()
    active_employees = db.query(func.count(Employee.id)).filter(Employee.status == EmployeeStatusEnum.ACTIVE).scalar()
    
    total_tickets = db.query(func.count(MaintenanceTicket.id)).scalar()
    open_tickets = db.query(func.count(MaintenanceTicket.id)).filter(MaintenanceTicket.status.in_([TicketStatusEnum.OPEN, TicketStatusEnum.IN_PROGRESS])).scalar()
    
    return {
        "assets": {"total": total_assets, "online": online_assets},
        "employees": {"total": total_employees, "active": active_employees},
        "tickets": {"total": total_tickets, "open": open_tickets}
    }

@router.get("/assets")
def get_assets_stats(db: Session = Depends(deps.get_db)) -> Any:
    status_counts = db.query(Device.status, func.count(Device.id)).group_by(Device.status).all()
    lifecycle_counts = db.query(Device.lifecycle_status, func.count(Device.id)).group_by(Device.lifecycle_status).all()
    
    return {
        "by_status": {k.value: v for k, v in status_counts},
        "by_lifecycle": {k: v for k, v in lifecycle_counts if k is not None}
    }

@router.get("/maintenance")
def get_maintenance_stats(db: Session = Depends(deps.get_db)) -> Any:
    status_counts = db.query(MaintenanceTicket.status, func.count(MaintenanceTicket.id)).group_by(MaintenanceTicket.status).all()
    priority_counts = db.query(MaintenanceTicket.priority, func.count(MaintenanceTicket.id)).group_by(MaintenanceTicket.priority).all()
    
    return {
        "by_status": {k.value: v for k, v in status_counts},
        "by_priority": {k.value: v for k, v in priority_counts}
    }
'''
with open("backend/app/api/v1/endpoints/dashboard.py", "w") as f:
    f.write(dashboard_code)

api_py = "backend/app/api/v1/api.py"
with open(api_py, "r") as f:
    api_content = f.read()

if "dashboard" not in api_content:
    api_content = api_content.replace("from app.api.v1.endpoints import (", "from app.api.v1.endpoints import (\n    dashboard,")
    api_content += "\napi_router.include_router(dashboard.router, prefix=\"/dashboard\", tags=[\"dashboard\"])\n"
    with open(api_py, "w") as f:
        f.write(api_content)

print("Phase 9 completed")
