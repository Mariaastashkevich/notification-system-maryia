from channels.email_channel import EmailChannel
from channels.settings import ChannelSettings
from channels.sms_channel import SMSChannel
from core.notification_message import Priority
from core.notification_router import RouterConfig, NotificationRouter
from notification_service import NotificationService
from observer_event_system.event_dispatcher import EventDispatcher
from observer_event_system.listeners.log_listener import LogListener


def get_notification_service() -> NotificationService:
    channels_settings = ChannelSettings()

    sms_channel = SMSChannel(settings=channels_settings)
    email_channel = EmailChannel(settings=channels_settings)

    channels = {
        "sms": sms_channel,
        "email": email_channel
    }

    router_config = RouterConfig(
        channel_priority={
            Priority.LOW: ['sms'],
            Priority.NORMAL: ['sms'],
            Priority.HIGH: ['sms', 'email'],
            Priority.CRITICAL: ['sms', 'email']},
        fallback_enabled=True
    )

    router = NotificationRouter(channels, router_config)

    dispatcher = EventDispatcher()
    log_listener = LogListener()
    dispatcher.attach(log_listener)

    return NotificationService(
        router=router,
        dispatcher=dispatcher,
    )
