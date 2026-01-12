from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from core.notification_result import Status

@dataclass(frozen=True)
class ChannelResult:
    status: Status
    error_message: Optional[str]
    sent_at: Optional[datetime]

    @classmethod
    def sent(cls):
        return cls(
            Status.SENT,
            None,
            datetime.now(timezone.utc),
        )

    @classmethod
    def failed(cls, error_message: Optional[str]):
        return cls(
            Status.FAILED,
            error_message,
            None,
        )