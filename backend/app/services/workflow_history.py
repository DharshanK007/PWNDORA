from sqlalchemy.orm import Session
from app.models.workflow_history import WorkflowHistory
from app.schemas.workflow_history import WorkflowHistoryCreate
from typing import List

class WorkflowHistoryService:
    @staticmethod
    def record_transition(db: Session, obj_in: WorkflowHistoryCreate) -> WorkflowHistory:
        obj_in_data = obj_in.model_dump()
        db_obj = WorkflowHistory(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    @staticmethod
    def get_history_for_entity(db: Session, entity: str, entity_id: str) -> List[WorkflowHistory]:
        return db.query(WorkflowHistory).filter(
            WorkflowHistory.entity == entity,
            WorkflowHistory.entity_id == entity_id
        ).order_by(WorkflowHistory.transition_time.desc()).all()
