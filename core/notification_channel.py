from core.channel_result import ChannelResult
from core.notification_message import NotificationMessage
from abc import ABC, abstractmethod

from core.notification_result import NotificationResult


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message: NotificationMessage) -> ChannelResult:
        pass

