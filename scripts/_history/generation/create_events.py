import os

base_dir = "backend/app/events"
os.makedirs(base_dir, exist_ok=True)

# base_event.py
with open(os.path.join(base_dir, "base_event.py"), "w") as f:
    f.write('''from datetime import datetime, timezone
from uuid import uuid4
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class BaseEvent(BaseModel):
    event_id: str
    event_name: str
    entity: str
    entity_id: str
    actor: Optional[str] = None
    timestamp: datetime
    metadata: Dict[str, Any] = {}
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def create(cls, entity_id: str, entity: str = None, actor: Optional[str] = None, metadata: Dict[str, Any] = None):
        return cls(
            event_id=str(uuid4()),
            event_name=cls.__name__,
            entity=entity or cls.__name__.lower(),
            entity_id=entity_id,
            actor=actor,
            timestamp=datetime.now(timezone.utc),
            metadata=metadata or {}
        )
''')

# events.py
with open(os.path.join(base_dir, "events.py"), "w") as f:
    f.write('''from app.events.base_event import BaseEvent

# Employee Events
class EmployeeActivated(BaseEvent): pass
class EmployeeTerminated(BaseEvent): pass

# Device Events
class DeviceRegistered(BaseEvent): pass
class DeviceConfigured(BaseEvent): pass
class DeviceActivated(BaseEvent): pass
class DeviceDecommissioned(BaseEvent): pass

# Firmware Events
class FirmwareSubmitted(BaseEvent): pass
class FirmwareApproved(BaseEvent): pass
class FirmwareDeployed(BaseEvent): pass
class FirmwareRollback(BaseEvent): pass

# Ticket Events
class TicketCreated(BaseEvent): pass
class TicketAssigned(BaseEvent): pass
class TicketStarted(BaseEvent): pass
class TicketResolved(BaseEvent): pass
class TicketClosed(BaseEvent): pass

# Inventory Events
class InventoryAllocated(BaseEvent): pass
class InventoryConsumed(BaseEvent): pass

# Report Events
class ReportPublished(BaseEvent): pass
class ReportArchived(BaseEvent): pass

# Auth Events
class LoginEvent(BaseEvent): pass
class FailedLoginEvent(BaseEvent): pass
class LogoutEvent(BaseEvent): pass
''')

# event_registry.py
with open(os.path.join(base_dir, "event_registry.py"), "w") as f:
    f.write('''class EventRegistry:
    def __init__(self):
        self._subscribers = {}
        
    def register(self, event_name: str, handler_func):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler_func)

    def get_subscribers(self, event_name: str):
        return self._subscribers.get(event_name, [])

registry = EventRegistry()
''')

# event_bus.py
with open(os.path.join(base_dir, "event_bus.py"), "w") as f:
    f.write('''from app.events.event_registry import registry
from app.events.base_event import BaseEvent
from fastapi import BackgroundTasks

class EventBus:
    @staticmethod
    def publish(event: BaseEvent, background_tasks: BackgroundTasks = None):
        handlers = registry.get_subscribers(event.event_name)
        for handler in handlers:
            if background_tasks:
                background_tasks.add_task(handler, event)
            else:
                handler(event)
''')

# handlers.py
with open(os.path.join(base_dir, "handlers.py"), "w") as f:
    f.write('''from app.events.base_event import BaseEvent
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
    from app.services.notification import NotificationService
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

register_all_handlers()
''')

# __init__.py
with open(os.path.join(base_dir, "__init__.py"), "w") as f:
    f.write('''# import handlers to trigger registration
import app.events.handlers
''')

print("Created event files.")
