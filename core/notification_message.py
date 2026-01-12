import datetime
import uuid
from enum import Enum
from typing import List
from dataclasses import dataclass

class Priority(Enum):
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    CRITICAL = 'critical'

@dataclass(frozen=True)
class NotificationMessage:
    id: uuid.UUID
    user_id: str
    message: str
    priority: Priority
    channels_requested: List[str]
    created_at: datetime.datetime


