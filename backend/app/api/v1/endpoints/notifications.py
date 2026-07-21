from app.api.dependencies.query import QueryParameters, get_query_parameters
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.services.notification import notification
from app.schemas.notification import NotificationResponse, NotificationUpdate
from app.schemas.base import PagedResponse
from app.models.user import RoleEnum

router = APIRouter()

@router.get("/", response_model=PagedResponse[NotificationResponse])
def read_notifications(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve notifications for current user.
    """
    items = db.query(notification.model).filter(
        notification.model.recipient_id == str(current_user.id)
    ).offset(skip).limit(limit).all()
    
    total = db.query(notification.model).filter(
        notification.model.recipient_id == str(current_user.id)
    ).count()
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.patch("/{id}/read", response_model=NotificationResponse)
def mark_notification_read(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Mark a notification as read.
    """
    item = notification.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Notification not found")
    if item.recipient_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return notification.mark_read(db, db_obj=item)
