from app.events.event_registry import registry
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
