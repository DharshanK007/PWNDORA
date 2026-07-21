from datetime import datetime, timezone
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
