import uuid

from api.schemas.notification import NotificationResponse
from core.notification_message import NotificationMessage
from core.notification_result import Status
from core.notification_router import NotificationRouter
from db.enums import NotificationStatus
from db.models.notification import NotificationsOrm
from db.session import session_factory
from observer_event_system.event_dispatcher import EventDispatcher
from observer_event_system.notification_event import NotificationEvent


class NotificationService:
    def __init__(self, router: NotificationRouter, dispatcher: EventDispatcher):
        self.router = router
        self.dispatcher = dispatcher

    def send_notification(self, message: NotificationMessage) -> NotificationResponse:
        notification = NotificationsOrm(
            id=message.id,
            user_id=message.user_id,
            message=message.message,
            channels_requested=message.channels_requested,
            channel_used=None,
            priority=message.priority,
            status=NotificationStatus.PENDING,
            error_message=None,
            created_at=message.created_at,
            sent_at=None,
        )
        with session_factory() as session:
            session.add(notification)
            session.commit()
            session.refresh(notification)
            router_result = self.router.route(message)
            if router_result.status == Status.SENT:
                notification.status = NotificationStatus.SENT
                notification.channel_used = router_result.channel_used
                notification.sent_at = router_result.sent_at
                event = NotificationEvent(
                    notification_id=notification.id,
                    user_id=notification.user_id,
                    status=Status.SENT,
                    channel=router_result.channel_used,
                    sent_at=router_result.sent_at,
                )
                self.dispatcher.notify(event)
            elif router_result.status == Status.FAILED:
                notification.status = NotificationStatus.FAILED
                notification.channel_used = router_result.channel_used
                notification.error_message = router_result.error_message
                event = NotificationEvent(
                    notification_id=notification.id,
                    user_id=notification.user_id,
                    status=Status.FAILED,
                    channel=router_result.channel_used,
                    error_message=router_result.error_message,
                )
                self.dispatcher.notify(event)
            session.commit()
            session.refresh(notification)
            return NotificationResponse.model_validate(notification)

    @staticmethod
    def get_notification(notification_id: uuid.UUID) -> NotificationResponse | None:
        with session_factory() as session:
            notification = (
                    session
                    .query(NotificationsOrm)
                    .filter(NotificationsOrm.id == notification_id)
                    .one_or_none()
                )
            if notification is None:
                return None
            else:
                return NotificationResponse.model_validate(notification)








