from typing import Any
from app.events.base_event import BaseEvent
from app.db.session import SessionLocal
from app.models.user import User
from app.models.learner_capability import LearnerCapability
from app.scenarios.scenario_manager import manager
import logging

logger = logging.getLogger(__name__)

def record_capability(db, user_id: str, capability: str, scenario_id: str = "operation_phantom_firmware", stage_id: int = 1):
    if not capability or not user_id:
        return
    try:
        new_cap = LearnerCapability(
            user_id=str(user_id),
            capability=capability,
            scenario_id=scenario_id,
            stage_id=stage_id
        )
        db.add(new_cap)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to insert LearnerCapability record: {e}")

def capability_tracker_handler(event: BaseEvent):
    """
    Subscribes to StageAdvanced.
    Reads capability_gained from event metadata/stage config and appends it to LearnerCapability table and User.capabilities.
    """
    if event.event_name != "StageAdvanced":
        return

    db = SessionLocal()
    try:
        scenario_id = event.metadata.get("scenario_id")
        stage_id = event.metadata.get("stage_id")
        user_id = event.actor or event.metadata.get("user_id")

        if not scenario_id or stage_id is None or not user_id:
            return

        scenario_config = manager.registry.get_scenario(scenario_id)
        capability = event.metadata.get("capability_gained")
        if not capability and scenario_config:
            stage_config = next((s for s in scenario_config.get("stages", []) if s.get("id") == stage_id), None)
            if stage_config:
                capability = stage_config.get("capability_gained")

        if not capability:
            return

        # 1. Store in LearnerCapability table
        record_capability(db, str(user_id), capability, str(scenario_id), int(stage_id))

        # 2. Store in User.capabilities JSON
        user = db.query(User).filter(User.id == str(user_id)).first()
        if user:
            caps = dict(user.capabilities or {})
            if capability not in caps:
                caps[capability] = {
                    "scenario_id": scenario_id,
                    "stage_id": stage_id,
                    "acquired_at": event.timestamp.isoformat()
                }
                user.capabilities = caps
                db.commit()

    except Exception as e:
        logger.error(f"Failed to track capability for event {event.event_name}: {e}")
    finally:
        db.close()

def register_capability_tracker():
    from app.events.event_registry import registry as event_registry
    event_registry.register("StageAdvanced", capability_tracker_handler)

register_capability_tracker()
