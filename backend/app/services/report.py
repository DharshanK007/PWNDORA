from sqlalchemy.orm import Session
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
