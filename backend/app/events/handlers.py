from app.events.base_event import BaseEvent
from app.db.session import SessionLocal
import logging

logger = logging.getLogger(__name__)

def audit_log_handler(event: BaseEvent):
    from app.audit.audit_service import AuditService
    from app.audit.audit_schema import AuditLogCreate
    
    db = SessionLocal()
    try:
        log_data = AuditLogCreate(
            actor_user_id=event.actor,
            target_entity=event.entity,
            target_entity_id=event.entity_id,
            action=event.event_name,
            previous_state=event.metadata.get("previous_state"),
            new_state=event.metadata.get("new_state"),
            payload=event.model_dump(mode="json")
        )
        AuditService.log_action(db, log_data)
    except Exception as e:
        logger.error(f"Failed to write audit log for event {event.event_name}: {e}")
    finally:
        db.close()

def notification_handler(event: BaseEvent):
    from app.services.notification import notification
    from app.schemas.notification import NotificationCreate, NotificationSeverityEnum
    
    # We only generate notifications for specific events
    # This logic will be fleshed out in Phase 3
    pass

def workflow_history_handler(event: BaseEvent):
    from app.services.workflow_history import WorkflowHistoryService
    from app.schemas.workflow_history import WorkflowHistoryCreate
    
    if "previous_state" in event.metadata and "new_state" in event.metadata:
        db = SessionLocal()
        try:
            history_data = WorkflowHistoryCreate(
                entity=event.entity,
                entity_id=event.entity_id,
                old_state=event.metadata.get("previous_state"),
                new_state=event.metadata.get("new_state"),
                triggered_by=event.actor,
                reason=event.metadata.get("reason"),
                transition_method=event.event_name,
                comments=event.metadata.get("comments")
            )
            WorkflowHistoryService.record_transition(db, history_data)
        except Exception as e:
            logger.error(f"Failed to write workflow history for event {event.event_name}: {e}")
        finally:
            db.close()

def scenario_report_handler(event: BaseEvent):
    try:
        if event.event_name == "ScenarioCompleted":
            from app.report_generator import generate_scenario_report
            generate_scenario_report(event.entity_id, event.actor)
    except Exception as e:
        logger.error(f"Failed to trigger scenario report generator: {e}")



def register_all_handlers():
    from app.events.event_registry import registry
    from app.events import events
    
    # Register audit log handler to ALL events
    for name in dir(events):
        obj = getattr(events, name)
        if isinstance(obj, type) and issubclass(obj, BaseEvent) and obj is not BaseEvent:
            registry.register(name, audit_log_handler)
            registry.register(name, notification_handler)
            registry.register(name, workflow_history_handler)
            
    registry.register("ScenarioCompleted", scenario_report_handler)

register_all_handlers()
