import logging
import random

from core.channel_result import ChannelResult
from core.notification_channel import NotificationChannel
from core.notification_message import NotificationMessage
from core.notification_result import NotificationResult
from channels.settings import ChannelSettings

logger = logging.getLogger(__name__)


class SMSChannel(NotificationChannel):
    def __init__(self, settings: ChannelSettings):
        self.settings = settings

    def send(self, message: NotificationMessage) -> ChannelResult:
        is_failed = random.random() < self.settings.sms_failure_rate

        if self.settings.sms_enabled:
            logger.info(
                f"Trying to send message via SMS",
                extra={
                    "notification_id": str(message.id),
                    "user_id": str(message.user_id),
                    "priority": str(message.priority.value),
                }
            )
            if is_failed:
                logger.error("SMS provider error")
                return ChannelResult.failed("SMS provider error")
            logger.info("Successfully sent message via SMS")
            return ChannelResult.sent()

        logger.error("SMS channel is disabled by configuration")
        return ChannelResult.failed("SMS channel is disabled by configuration")






