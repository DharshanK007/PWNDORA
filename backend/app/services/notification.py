from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate
from app.services.base import CRUDBase

class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    def mark_read(self, db: Session, *, db_obj: Notification) -> Notification:
        db_obj.read_status = True
        db.commit()
        db.refresh(db_obj)
        return db_obj

notification = CRUDNotification(Notification)
