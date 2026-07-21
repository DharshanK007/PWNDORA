from app.models.activity_log import ActivityLog
from app.schemas.activity_log import ActivityLogCreate
from app.services.base import CRUDBase
from pydantic import BaseModel

class ActivityLogUpdateDummy(BaseModel):
    pass

class CRUDActivityLog(CRUDBase[ActivityLog, ActivityLogCreate, ActivityLogUpdateDummy]):
    pass

activity_log = CRUDActivityLog(ActivityLog)
