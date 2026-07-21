from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
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

@router.get("/organization")
def get_dashboard_organization(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated organization metrics"}

@router.get("/network")
def get_dashboard_network(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated network metrics"}

@router.get("/security")
def get_dashboard_security(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated security metrics"}

@router.get("/activity")
def get_dashboard_activity(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated activity metrics"}

@router.get("/operations")
def get_dashboard_operations(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated operations metrics"}

@router.get("/statistics")
def get_dashboard_statistics(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated statistics metrics"}
