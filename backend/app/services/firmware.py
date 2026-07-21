from sqlalchemy.orm import Session
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
