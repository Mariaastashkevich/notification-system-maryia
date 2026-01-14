from channels.email_channel import EmailChannel
from config.channels import ChannelSettings
from channels.sms_channel import SMSChannel
from config.router import RouterSettings
from core.notification_router import RouterConfig, NotificationRouter
from notification_service import NotificationService
from observer_event_system.event_dispatcher import EventDispatcher
from observer_event_system.listeners.log_listener import LogListener


def get_notification_service() -> NotificationService:
    channels_settings = ChannelSettings()
    router_settings = RouterSettings()

    sms_channel = SMSChannel(settings=channels_settings)
    email_channel = EmailChannel(settings=channels_settings)

    channels = {
        "sms": sms_channel,
        "email": email_channel
    }

    router_config = RouterConfig(
        channel_priority=router_settings.priority_to_dict(),
        fallback_enabled=router_settings.fallback_enabled,
    )

    router = NotificationRouter(channels, router_config)

    dispatcher = EventDispatcher()
    log_listener = LogListener()
    dispatcher.attach(log_listener)

    return NotificationService(
        router=router,
        dispatcher=dispatcher,
    )
