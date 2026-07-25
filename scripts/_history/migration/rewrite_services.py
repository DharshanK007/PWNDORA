import os

services = {
    "employee.py": '''from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.models.employee import Employee, EmployeeStatusEnum
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition
from app.events.event_bus import EventBus
from app.events.events import EmployeeActivated, EmployeeTerminated

class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def activate(self, db: Session, *, db_obj: Employee) -> Employee:
        old_state = db_obj.status.value
        validate_transition(old_state, EmployeeStatusEnum.ACTIVE.value, {
            EmployeeStatusEnum.PENDING.value: [EmployeeStatusEnum.ACTIVE.value],
            EmployeeStatusEnum.SUSPENDED.value: [EmployeeStatusEnum.ACTIVE.value]
        })
        require_condition(db_obj.department_id is not None, "Employee must have a department assigned")
        require_condition(db_obj.user_id is not None, "Employee must have a linked user account")
        db_obj.status = EmployeeStatusEnum.ACTIVE
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(EmployeeActivated.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def suspend(self, db: Session, *, db_obj: Employee) -> Employee:
        old_state = db_obj.status.value
        validate_transition(old_state, EmployeeStatusEnum.SUSPENDED.value, {
            EmployeeStatusEnum.ACTIVE.value: [EmployeeStatusEnum.SUSPENDED.value]
        })
        db_obj.status = EmployeeStatusEnum.SUSPENDED
        db.commit()
        db.refresh(db_obj)
        # EventBus.publish(EmployeeSuspended.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def terminate(self, db: Session, *, db_obj: Employee) -> Employee:
        old_state = db_obj.status.value
        validate_transition(old_state, EmployeeStatusEnum.TERMINATED.value, {
            EmployeeStatusEnum.ACTIVE.value: [EmployeeStatusEnum.TERMINATED.value],
            EmployeeStatusEnum.SUSPENDED.value: [EmployeeStatusEnum.TERMINATED.value],
            EmployeeStatusEnum.PENDING.value: [EmployeeStatusEnum.TERMINATED.value]
        })
        db_obj.status = EmployeeStatusEnum.TERMINATED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(EmployeeTerminated.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

employee = CRUDEmployee(Employee)
''',

    "device.py": '''from sqlalchemy.orm import Session
from app.models.device import Device, DeviceStatusEnum
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition
from app.events.event_bus import EventBus
from app.events.events import DeviceRegistered, DeviceConfigured, DeviceActivated, DeviceDecommissioned

class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    def register(self, db: Session, *, db_obj: Device) -> Device:
        old_state = db_obj.status.value
        validate_transition(old_state, DeviceStatusEnum.REGISTERED.value, {
            DeviceStatusEnum.NEW.value: [DeviceStatusEnum.REGISTERED.value]
        })
        db_obj.status = DeviceStatusEnum.REGISTERED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(DeviceRegistered.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def configure(self, db: Session, *, db_obj: Device) -> Device:
        old_state = db_obj.status.value
        validate_transition(old_state, DeviceStatusEnum.CONFIGURED.value, {
            DeviceStatusEnum.REGISTERED.value: [DeviceStatusEnum.CONFIGURED.value],
            DeviceStatusEnum.MAINTENANCE.value: [DeviceStatusEnum.CONFIGURED.value]
        })
        require_condition(db_obj.firmware_id is not None, "Device cannot become CONFIGURED unless firmware exists.")
        db_obj.status = DeviceStatusEnum.CONFIGURED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(DeviceConfigured.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def activate(self, db: Session, *, db_obj: Device) -> Device:
        old_state = db_obj.status.value
        validate_transition(old_state, DeviceStatusEnum.ONLINE.value, {
            DeviceStatusEnum.CONFIGURED.value: [DeviceStatusEnum.ONLINE.value],
            DeviceStatusEnum.OFFLINE.value: [DeviceStatusEnum.ONLINE.value],
            DeviceStatusEnum.MAINTENANCE.value: [DeviceStatusEnum.ONLINE.value]
        })
        require_condition(db_obj.firmware_id is not None, "Device must be configured with firmware.")
        require_condition(db_obj.location_id is not None, "Device must be assigned to a machine location.")
        db_obj.status = DeviceStatusEnum.ONLINE
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(DeviceActivated.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def decommission(self, db: Session, *, db_obj: Device) -> Device:
        old_state = db_obj.status.value
        db_obj.status = DeviceStatusEnum.DECOMMISSIONED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(DeviceDecommissioned.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

device = CRUDDevice(Device)
''',

    "firmware.py": '''from sqlalchemy.orm import Session
from app.models.firmware import Firmware, FirmwareStatusEnum
from app.schemas.firmware import FirmwareCreate, FirmwareUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition
from app.events.event_bus import EventBus
from app.events.events import FirmwareSubmitted, FirmwareApproved, FirmwareDeployed, FirmwareRollback

class CRUDFirmware(CRUDBase[Firmware, FirmwareCreate, FirmwareUpdate]):
    def submit(self, db: Session, *, db_obj: Firmware) -> Firmware:
        old_state = db_obj.status.value
        validate_transition(old_state, FirmwareStatusEnum.PENDING_APPROVAL.value, {
            FirmwareStatusEnum.DRAFT.value: [FirmwareStatusEnum.PENDING_APPROVAL.value]
        })
        db_obj.status = FirmwareStatusEnum.PENDING_APPROVAL
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(FirmwareSubmitted.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def approve(self, db: Session, *, db_obj: Firmware) -> Firmware:
        old_state = db_obj.status.value
        validate_transition(old_state, FirmwareStatusEnum.APPROVED.value, {
            FirmwareStatusEnum.PENDING_APPROVAL.value: [FirmwareStatusEnum.APPROVED.value]
        })
        db_obj.status = FirmwareStatusEnum.APPROVED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(FirmwareApproved.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def deploy(self, db: Session, *, db_obj: Firmware) -> Firmware:
        old_state = db_obj.status.value
        validate_transition(old_state, FirmwareStatusEnum.DEPLOYED.value, {
            FirmwareStatusEnum.APPROVED.value: [FirmwareStatusEnum.DEPLOYED.value]
        })
        db_obj.status = FirmwareStatusEnum.DEPLOYED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(FirmwareDeployed.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def rollback(self, db: Session, *, db_obj: Firmware) -> Firmware:
        old_state = db_obj.status.value
        validate_transition(old_state, FirmwareStatusEnum.RETIRED.value, {
            FirmwareStatusEnum.DEPLOYED.value: [FirmwareStatusEnum.RETIRED.value]
        })
        db_obj.status = FirmwareStatusEnum.RETIRED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(FirmwareRollback.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

firmware = CRUDFirmware(Firmware)
''',

    "maintenance_ticket.py": '''from sqlalchemy.orm import Session
from app.models.maintenance_ticket import MaintenanceTicket, TicketStatusEnum
from app.schemas.maintenance_ticket import MaintenanceTicketCreate, MaintenanceTicketUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition
from uuid import UUID
from app.events.event_bus import EventBus
from app.events.events import TicketAssigned, TicketStarted, TicketResolved, TicketClosed

class CRUDMaintenanceTicket(CRUDBase[MaintenanceTicket, MaintenanceTicketCreate, MaintenanceTicketUpdate]):
    def assign(self, db: Session, *, db_obj: MaintenanceTicket, engineer_id: UUID) -> MaintenanceTicket:
        old_state = db_obj.status.value
        validate_transition(old_state, TicketStatusEnum.ASSIGNED.value, {
            TicketStatusEnum.OPEN.value: [TicketStatusEnum.ASSIGNED.value]
        })
        db_obj.assigned_to_id = str(engineer_id)
        db_obj.status = TicketStatusEnum.ASSIGNED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(TicketAssigned.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def start(self, db: Session, *, db_obj: MaintenanceTicket) -> MaintenanceTicket:
        old_state = db_obj.status.value
        validate_transition(old_state, TicketStatusEnum.IN_PROGRESS.value, {
            TicketStatusEnum.ASSIGNED.value: [TicketStatusEnum.IN_PROGRESS.value]
        })
        db_obj.status = TicketStatusEnum.IN_PROGRESS
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(TicketStarted.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def resolve(self, db: Session, *, db_obj: MaintenanceTicket, resolution_notes: str) -> MaintenanceTicket:
        old_state = db_obj.status.value
        validate_transition(old_state, TicketStatusEnum.RESOLVED.value, {
            TicketStatusEnum.IN_PROGRESS.value: [TicketStatusEnum.RESOLVED.value]
        })
        db_obj.resolution_notes = resolution_notes
        db_obj.status = TicketStatusEnum.RESOLVED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(TicketResolved.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def close(self, db: Session, *, db_obj: MaintenanceTicket) -> MaintenanceTicket:
        old_state = db_obj.status.value
        validate_transition(old_state, TicketStatusEnum.CLOSED.value, {
            TicketStatusEnum.RESOLVED.value: [TicketStatusEnum.CLOSED.value]
        })
        db_obj.status = TicketStatusEnum.CLOSED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(TicketClosed.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

maintenance_ticket = CRUDMaintenanceTicket(MaintenanceTicket)
''',

    "inventory.py": '''from sqlalchemy.orm import Session
from app.models.inventory import Inventory, InventoryStatusEnum
from app.schemas.inventory import InventoryCreate, InventoryUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition
from app.events.event_bus import EventBus
from app.events.events import InventoryAllocated, InventoryConsumed

class CRUDInventory(CRUDBase[Inventory, InventoryCreate, InventoryUpdate]):
    def allocate(self, db: Session, *, db_obj: Inventory, quantity: int) -> Inventory:
        old_state = db_obj.status.value
        validate_transition(old_state, InventoryStatusEnum.ALLOCATED.value, {
            InventoryStatusEnum.CREATED.value: [InventoryStatusEnum.ALLOCATED.value],
            InventoryStatusEnum.AVAILABLE.value: [InventoryStatusEnum.ALLOCATED.value],
            InventoryStatusEnum.RESTOCKED.value: [InventoryStatusEnum.ALLOCATED.value]
        })
        require_condition(db_obj.stock_quantity >= quantity, "Insufficient stock for allocation")
        db_obj.stock_quantity -= quantity
        db_obj.status = InventoryStatusEnum.ALLOCATED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(InventoryAllocated.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def consume(self, db: Session, *, db_obj: Inventory) -> Inventory:
        old_state = db_obj.status.value
        validate_transition(old_state, InventoryStatusEnum.CONSUMED.value, {
            InventoryStatusEnum.ALLOCATED.value: [InventoryStatusEnum.CONSUMED.value]
        })
        db_obj.status = InventoryStatusEnum.CONSUMED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(InventoryConsumed.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj
        
    def restock(self, db: Session, *, db_obj: Inventory, quantity: int) -> Inventory:
        old_state = db_obj.status.value
        db_obj.stock_quantity += quantity
        db_obj.status = InventoryStatusEnum.RESTOCKED
        db.commit()
        db.refresh(db_obj)
        return db_obj

inventory = CRUDInventory(Inventory)
''',

    "report.py": '''from sqlalchemy.orm import Session
from app.models.report import Report, ReportStatusEnum
from app.schemas.report import ReportCreate, ReportUpdate
from app.services.base import CRUDBase
from app.core.workflows import validate_transition, require_condition
from app.events.event_bus import EventBus
from app.events.events import ReportPublished, ReportArchived

class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def publish(self, db: Session, *, db_obj: Report) -> Report:
        old_state = db_obj.status.value
        validate_transition(old_state, ReportStatusEnum.PUBLISHED.value, {
            ReportStatusEnum.APPROVED.value: [ReportStatusEnum.PUBLISHED.value]
        })
        db_obj.status = ReportStatusEnum.PUBLISHED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(ReportPublished.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def archive(self, db: Session, *, db_obj: Report) -> Report:
        old_state = db_obj.status.value
        db_obj.status = ReportStatusEnum.ARCHIVED
        db.commit()
        db.refresh(db_obj)
        EventBus.publish(ReportArchived.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

    def approve(self, db: Session, *, db_obj: Report) -> Report:
        old_state = db_obj.status.value
        validate_transition(old_state, ReportStatusEnum.APPROVED.value, {
            ReportStatusEnum.DRAFT.value: [ReportStatusEnum.APPROVED.value],
            ReportStatusEnum.UNDER_REVIEW.value: [ReportStatusEnum.APPROVED.value]
        })
        db_obj.status = ReportStatusEnum.APPROVED
        db.commit()
        db.refresh(db_obj)
        # EventBus.publish(ReportApproved.create(entity_id=str(db_obj.id), metadata={"previous_state": old_state, "new_state": db_obj.status.value}))
        return db_obj

report = CRUDReport(Report)
'''
}

base_dir = "backend/app/services"
for filename, content in services.items():
    with open(os.path.join(base_dir, filename), "w") as f:
        f.write(content)

print("Refactored services.")
