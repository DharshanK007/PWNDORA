from typing import Any, Dict, Optional, Union
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
