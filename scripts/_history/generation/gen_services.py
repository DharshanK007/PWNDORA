import os

services_dir = "backend/app/services"

# Employee Service
employee_content = '''from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.models.employee import Employee, EmployeeStatusEnum
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition

class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def activate(self, db: Session, *, db_obj: Employee) -> Employee:
        validate_transition(db_obj.status.value, EmployeeStatusEnum.ACTIVE.value, {
            EmployeeStatusEnum.PENDING.value: [EmployeeStatusEnum.ACTIVE.value],
            EmployeeStatusEnum.SUSPENDED.value: [EmployeeStatusEnum.ACTIVE.value]
        })
        require_condition(db_obj.department_id is not None, "Employee must have a department assigned")
        require_condition(db_obj.user_id is not None, "Employee must have a linked user account")
        db_obj.status = EmployeeStatusEnum.ACTIVE
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def suspend(self, db: Session, *, db_obj: Employee) -> Employee:
        validate_transition(db_obj.status.value, EmployeeStatusEnum.SUSPENDED.value, {
            EmployeeStatusEnum.ACTIVE.value: [EmployeeStatusEnum.SUSPENDED.value]
        })
        db_obj.status = EmployeeStatusEnum.SUSPENDED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def terminate(self, db: Session, *, db_obj: Employee) -> Employee:
        validate_transition(db_obj.status.value, EmployeeStatusEnum.TERMINATED.value, {
            EmployeeStatusEnum.ACTIVE.value: [EmployeeStatusEnum.TERMINATED.value],
            EmployeeStatusEnum.SUSPENDED.value: [EmployeeStatusEnum.TERMINATED.value],
            EmployeeStatusEnum.PENDING.value: [EmployeeStatusEnum.TERMINATED.value]
        })
        db_obj.status = EmployeeStatusEnum.TERMINATED
        db.commit()
        db.refresh(db_obj)
        return db_obj

employee = CRUDEmployee(Employee)
'''
with open(f"{services_dir}/employee.py", "w") as f:
    f.write(employee_content)


# Device Service
device_content = '''from sqlalchemy.orm import Session
from app.models.device import Device, DeviceStatusEnum
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition

class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    def register(self, db: Session, *, db_obj: Device) -> Device:
        validate_transition(db_obj.status.value, DeviceStatusEnum.REGISTERED.value, {
            DeviceStatusEnum.NEW.value: [DeviceStatusEnum.REGISTERED.value]
        })
        db_obj.status = DeviceStatusEnum.REGISTERED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def configure(self, db: Session, *, db_obj: Device) -> Device:
        validate_transition(db_obj.status.value, DeviceStatusEnum.CONFIGURED.value, {
            DeviceStatusEnum.REGISTERED.value: [DeviceStatusEnum.CONFIGURED.value],
            DeviceStatusEnum.MAINTENANCE.value: [DeviceStatusEnum.CONFIGURED.value]
        })
        require_condition(db_obj.firmware_id is not None, "Device cannot become CONFIGURED unless firmware exists.")
        db_obj.status = DeviceStatusEnum.CONFIGURED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def activate(self, db: Session, *, db_obj: Device) -> Device:
        validate_transition(db_obj.status.value, DeviceStatusEnum.ONLINE.value, {
            DeviceStatusEnum.CONFIGURED.value: [DeviceStatusEnum.ONLINE.value],
            DeviceStatusEnum.OFFLINE.value: [DeviceStatusEnum.ONLINE.value],
            DeviceStatusEnum.MAINTENANCE.value: [DeviceStatusEnum.ONLINE.value]
        })
        require_condition(db_obj.firmware_id is not None, "Device must be configured with firmware.")
        require_condition(db_obj.location_id is not None, "Device must be assigned to a machine location.")
        db_obj.status = DeviceStatusEnum.ONLINE
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def decommission(self, db: Session, *, db_obj: Device) -> Device:
        # Can decommission from any state mostly
        db_obj.status = DeviceStatusEnum.DECOMMISSIONED
        db.commit()
        db.refresh(db_obj)
        return db_obj

device = CRUDDevice(Device)
'''
with open(f"{services_dir}/device.py", "w") as f:
    f.write(device_content)


# Firmware Service
firmware_content = '''from sqlalchemy.orm import Session
from app.models.firmware import Firmware, FirmwareStatusEnum
from app.schemas.firmware import FirmwareCreate, FirmwareUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition

class CRUDFirmware(CRUDBase[Firmware, FirmwareCreate, FirmwareUpdate]):
    def submit(self, db: Session, *, db_obj: Firmware) -> Firmware:
        validate_transition(db_obj.status.value, FirmwareStatusEnum.PENDING_APPROVAL.value, {
            FirmwareStatusEnum.DRAFT.value: [FirmwareStatusEnum.PENDING_APPROVAL.value]
        })
        db_obj.status = FirmwareStatusEnum.PENDING_APPROVAL
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def approve(self, db: Session, *, db_obj: Firmware) -> Firmware:
        validate_transition(db_obj.status.value, FirmwareStatusEnum.APPROVED.value, {
            FirmwareStatusEnum.PENDING_APPROVAL.value: [FirmwareStatusEnum.APPROVED.value]
        })
        db_obj.status = FirmwareStatusEnum.APPROVED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def deploy(self, db: Session, *, db_obj: Firmware) -> Firmware:
        validate_transition(db_obj.status.value, FirmwareStatusEnum.DEPLOYED.value, {
            FirmwareStatusEnum.APPROVED.value: [FirmwareStatusEnum.DEPLOYED.value]
        })
        db_obj.status = FirmwareStatusEnum.DEPLOYED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def rollback(self, db: Session, *, db_obj: Firmware) -> Firmware:
        validate_transition(db_obj.status.value, FirmwareStatusEnum.RETIRED.value, {
            FirmwareStatusEnum.DEPLOYED.value: [FirmwareStatusEnum.RETIRED.value]
        })
        db_obj.status = FirmwareStatusEnum.RETIRED
        db.commit()
        db.refresh(db_obj)
        return db_obj

firmware = CRUDFirmware(Firmware)
'''
with open(f"{services_dir}/firmware.py", "w") as f:
    f.write(firmware_content)


# Ticket Service
ticket_content = '''from sqlalchemy.orm import Session
from app.models.maintenance_ticket import MaintenanceTicket, TicketStatusEnum
from app.schemas.maintenance_ticket import MaintenanceTicketCreate, MaintenanceTicketUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition
from uuid import UUID

class CRUDMaintenanceTicket(CRUDBase[MaintenanceTicket, MaintenanceTicketCreate, MaintenanceTicketUpdate]):
    def assign(self, db: Session, *, db_obj: MaintenanceTicket, engineer_id: UUID) -> MaintenanceTicket:
        validate_transition(db_obj.status.value, TicketStatusEnum.ASSIGNED.value, {
            TicketStatusEnum.OPEN.value: [TicketStatusEnum.ASSIGNED.value]
        })
        db_obj.assigned_to_id = str(engineer_id)
        db_obj.status = TicketStatusEnum.ASSIGNED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def start(self, db: Session, *, db_obj: MaintenanceTicket) -> MaintenanceTicket:
        validate_transition(db_obj.status.value, TicketStatusEnum.IN_PROGRESS.value, {
            TicketStatusEnum.ASSIGNED.value: [TicketStatusEnum.IN_PROGRESS.value]
        })
        db_obj.status = TicketStatusEnum.IN_PROGRESS
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def resolve(self, db: Session, *, db_obj: MaintenanceTicket, resolution_notes: str) -> MaintenanceTicket:
        validate_transition(db_obj.status.value, TicketStatusEnum.RESOLVED.value, {
            TicketStatusEnum.IN_PROGRESS.value: [TicketStatusEnum.RESOLVED.value]
        })
        db_obj.resolution_notes = resolution_notes
        db_obj.status = TicketStatusEnum.RESOLVED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def close(self, db: Session, *, db_obj: MaintenanceTicket) -> MaintenanceTicket:
        validate_transition(db_obj.status.value, TicketStatusEnum.CLOSED.value, {
            TicketStatusEnum.RESOLVED.value: [TicketStatusEnum.CLOSED.value]
        })
        db_obj.status = TicketStatusEnum.CLOSED
        db.commit()
        db.refresh(db_obj)
        return db_obj

maintenance_ticket = CRUDMaintenanceTicket(MaintenanceTicket)
'''
with open(f"{services_dir}/maintenance_ticket.py", "w") as f:
    f.write(ticket_content)


# Inventory Service
inventory_content = '''from sqlalchemy.orm import Session
from app.models.inventory import Inventory, InventoryStatusEnum
from app.schemas.inventory import InventoryCreate, InventoryUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition

class CRUDInventory(CRUDBase[Inventory, InventoryCreate, InventoryUpdate]):
    def allocate(self, db: Session, *, db_obj: Inventory, quantity: int) -> Inventory:
        validate_transition(db_obj.status.value, InventoryStatusEnum.ALLOCATED.value, {
            InventoryStatusEnum.CREATED.value: [InventoryStatusEnum.ALLOCATED.value],
            InventoryStatusEnum.AVAILABLE.value: [InventoryStatusEnum.ALLOCATED.value],
            InventoryStatusEnum.RESTOCKED.value: [InventoryStatusEnum.ALLOCATED.value]
        })
        require_condition(db_obj.stock_quantity >= quantity, "Insufficient stock for allocation")
        db_obj.stock_quantity -= quantity
        db_obj.status = InventoryStatusEnum.ALLOCATED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def consume(self, db: Session, *, db_obj: Inventory) -> Inventory:
        validate_transition(db_obj.status.value, InventoryStatusEnum.CONSUMED.value, {
            InventoryStatusEnum.ALLOCATED.value: [InventoryStatusEnum.CONSUMED.value]
        })
        db_obj.status = InventoryStatusEnum.CONSUMED
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    def restock(self, db: Session, *, db_obj: Inventory, quantity: int) -> Inventory:
        db_obj.stock_quantity += quantity
        db_obj.status = InventoryStatusEnum.RESTOCKED
        db.commit()
        db.refresh(db_obj)
        return db_obj

inventory = CRUDInventory(Inventory)
'''
with open(f"{services_dir}/inventory.py", "w") as f:
    f.write(inventory_content)


# Report Service
report_content = '''from sqlalchemy.orm import Session
from app.models.report import Report, ReportStatusEnum
from app.schemas.report import ReportCreate, ReportUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition

class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def publish(self, db: Session, *, db_obj: Report) -> Report:
        validate_transition(db_obj.status.value, ReportStatusEnum.PUBLISHED.value, {
            ReportStatusEnum.APPROVED.value: [ReportStatusEnum.PUBLISHED.value]
        })
        db_obj.status = ReportStatusEnum.PUBLISHED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def archive(self, db: Session, *, db_obj: Report) -> Report:
        db_obj.status = ReportStatusEnum.ARCHIVED
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def approve(self, db: Session, *, db_obj: Report) -> Report:
        validate_transition(db_obj.status.value, ReportStatusEnum.APPROVED.value, {
            ReportStatusEnum.DRAFT.value: [ReportStatusEnum.APPROVED.value],
            ReportStatusEnum.UNDER_REVIEW.value: [ReportStatusEnum.APPROVED.value]
        })
        db_obj.status = ReportStatusEnum.APPROVED
        db.commit()
        db.refresh(db_obj)
        return db_obj

report = CRUDReport(Report)
'''
with open(f"{services_dir}/report.py", "w") as f:
    f.write(report_content)

print("Services updated.")
