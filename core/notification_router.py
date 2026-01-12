import logging
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

from core.channel_result import ChannelResult
from core.notification_channel import NotificationChannel
from core.notification_message import NotificationMessage, Priority
from core.notification_result import NotificationResult, Status

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RouterConfig:
    channel_priority: Dict[Priority, List[str]]
    fallback_enabled: bool


class NotificationRouter:
    def __init__(self, channels: Dict[str, NotificationChannel], config: RouterConfig):
        self.channels = channels
        self.config = config

    def route(self, message: NotificationMessage) -> NotificationResult:
        channels_order = self.config.channel_priority.get(message.priority, [])

        for channel in channels_order:
            if channel not in self.channels:
                continue
            logger.info(f"Trying to route {channel} from {channels_order}")
            channel_result: ChannelResult = self.channels.get(channel).send(message)

            if channel_result.status == Status.SENT:
                return self.build_result(channel_result, channel)
            elif channel_result.status == Status.FAILED:
                logger.error(f"Sending via channel {channel} failed")
                if not self.config.fallback_enabled:
                    return self.build_result(channel_result, channel)

        return NotificationResult(
            status=Status.FAILED,
            error_message=(
                f"Notification delivery failed"
                f"No available channels for priority: {message.priority.value}"
                f"Attempted channels: {channels_order}"
            ),
            sent_at=None,
            channel_used=None
        )

    @staticmethod
    def build_result(result: ChannelResult, channel: str) -> NotificationResult:
        return NotificationResult(
            status=result.status,
            error_message=result.error_message,
            sent_at=result.sent_at,
            channel_used=channel,
        )






