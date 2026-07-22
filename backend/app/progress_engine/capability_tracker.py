from typing import Any
from app.events.base_event import BaseEvent
from app.db.session import SessionLocal
from app.models.user import User
from app.scenarios.scenario_registry import registry
import logging

logger = logging.getLogger(__name__)

def capability_tracker_handler(event: BaseEvent):
    """
    Subscribes to StageAdvanced.
    Reads capability_gained from the stage configuration and appends it to User.capabilities.
    """
    if event.event_name != "StageAdvanced":
        return

    db = SessionLocal()
    try:
        scenario_id = event.metadata.get("scenario_id")
        stage_id = event.metadata.get("stage_id")
        user_id = event.actor

        if not scenario_id or not stage_id or not user_id:
            return

        scenario_config = registry.get_scenario(scenario_id)
        if not scenario_config:
            return

        stage_config = next((s for s in scenario_config.get("stages", []) if s.get("id") == stage_id), None)
        if not stage_config:
            return

        capability = stage_config.get("capability_gained")
        if not capability:
            return

        user = db.query(User).filter(User.id == user_id).first()
        if user:
            caps = user.capabilities or {}
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
