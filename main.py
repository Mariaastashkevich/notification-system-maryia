# import logging
# import uuid
# from datetime import datetime, timezone
# from api.app import create_app
# from db.models.audit_trail import AuditTrailOrm
# from channels.email_channel import EmailChannel
# from channels.settings import ChannelSettings
# from channels.sms_channel import SMSChannel
# from core.notification_message import Priority, NotificationMessage
# from core.notification_router import NotificationRouter, RouterConfig
# from db.dev.init_db import create_tables
# import logging
#
# from logging_config import configure_logging
# from notification_service import NotificationService
# from observer_event_system.event_dispatcher import EventDispatcher
# import observer_event_system.listeners.audit.sqlalchemy_hooks
# from observer_event_system.listeners.log_listener import LogListener
# def main():
#     configure_logging(level=logging.INFO)
#     create_tables()
#
#     channels_settings = ChannelSettings(
#         sms_enabled=True,
#         email_enabled=True,
#         sms_failure_rate=0.1,
#         email_failure_rate=0.05,
#     )
#
#     sms_channel = SMSChannel(settings=channels_settings)
#     email_channel = EmailChannel(settings=channels_settings)
#
#     channels = {
#         "sms": sms_channel,
#         "email": email_channel
#     }
#
#     router_config = RouterConfig(
#         channel_priority={
#         Priority.LOW: ['sms'],
#         Priority.NORMAL: ['sms'],
#         Priority.HIGH: ['sms', 'email'],
#         Priority.CRITICAL: ['sms', 'email']},
#         fallback_enabled=True
#     )
#
#     router = NotificationRouter(channels, router_config)
#
#     dispatcher = EventDispatcher()
#     log_listener = LogListener()
#     dispatcher.attach(log_listener)
#
#     service = NotificationService(
#         router=router,
#         dispatcher=dispatcher,
#     )
#
#     message = NotificationMessage(
#         id=uuid.uuid4(),
#         user_id="audit_test_user",
#         message="Hello audit trail",
#         priority=Priority.NORMAL,
#         channels_requested=["sms", "email"],
#         created_at=datetime.now(timezone.utc),
#     )
#     service.send_notification(message)



# if __name__ == "__main__":
from api.app import create_app
import logging
import observer_event_system.listeners.audit.sqlalchemy_hooks

from logging_config import configure_logging

configure_logging(level=logging.INFO)
app = create_app()
