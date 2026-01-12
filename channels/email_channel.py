import logging
import random

from core.channel_result import ChannelResult
from core.notification_channel import NotificationChannel
from core.notification_message import NotificationMessage
from core.notification_result import NotificationResult
from channels.settings import ChannelSettings

logger = logging.getLogger(__name__)


class EmailChannel(NotificationChannel):
    def __init__(self, settings: ChannelSettings):
        self.settings = settings

    def send(self, message: NotificationMessage) -> NotificationResult:
        is_failed = random.random() < self.settings.email_failure_rate

        if self.settings.email_enabled:
            logger.info(
                f"Trying to send message via Email",
                extra={
                    "notification_id": str(message.id),
                    "user_id": str(message.user_id),
                    "priority": str(message.priority.value),
                }
            )
            if is_failed:
                logger.error("Email provider error")
                return ChannelResult.failed("Email provider error")
            logger.info("Successfully sent message via Email")
            return ChannelResult.sent()

        logger.error("Email channel is disabled by configuration")
        return ChannelResult.failed("Email channel is disabled by configuration")


