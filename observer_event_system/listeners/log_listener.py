import logging

from core.notification_result import Status
from interfaces.event_listener import EventListener
from observer_event_system.notification_event import NotificationEvent

logger = logging.getLogger(__name__)


class LogListener(EventListener):
    def update(self, event_data: NotificationEvent):
        """
        Handles notification events and logs their result
        """
        match event_data.status:
            case Status.SENT:
                logger.info(f"Notification with id: {event_data.notification_id} success received at {event_data.sent_at}")
            case Status.FAILED:
                logger.info(f"Notification with id: {event_data.notification_id} failure received with error: {event_data.error_message}")
            case _:
                logger.error(f"Unknown event type: {event_data.status}")
