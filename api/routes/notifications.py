import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_notification_service
from api.schemas.notification import NotificationCreateRequest, NotificationResponse
from core.notification_message import NotificationMessage
# from db.models.notification import NotificationsOrm
from notification_service import NotificationService

router = APIRouter()
@router.post(
    "/notify",
        response_model=NotificationResponse
)
def send_notification(
        request: NotificationCreateRequest,
        service: NotificationService = Depends(get_notification_service),
):
    message = NotificationMessage(
        id=uuid.uuid4(),
        user_id=request.user_id,
        message=request.message,
        priority=request.priority,
        channels_requested=request.channels_requested,
        created_at=datetime.now(timezone.utc),
    )
    return service.send_notification(message)

@router.get(
    "/{notification_id}",
        response_model=NotificationResponse
)
def get_notification(
        notification_id: uuid.UUID,
        service: NotificationService = Depends(get_notification_service),
):
    notification = service.get_notification(notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    else:
        return notification

