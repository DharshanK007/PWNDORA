from sqlalchemy.orm import Session
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
