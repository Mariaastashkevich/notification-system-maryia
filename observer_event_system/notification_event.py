from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from core.notification_result import Status


@dataclass(frozen=True)
class NotificationEvent:
    notification_id: UUID
    user_id: str
    status: Status
    channel: Optional[str]
    error_message: Optional[str] = None
    sent_at: Optional[datetime] = None



