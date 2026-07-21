from sqlalchemy.orm import Session
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
