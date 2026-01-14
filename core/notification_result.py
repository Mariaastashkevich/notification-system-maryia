from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass

class Status(Enum):
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'

@dataclass(frozen=True)
class NotificationResult:
    status: Status
    error_message: Optional[str]
    sent_at: Optional[datetime]
    channel_used: Optional[str] = None
