from sqlalchemy.orm import Session
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
