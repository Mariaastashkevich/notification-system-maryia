import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from core.notification_message import Priority
from core.notification_result import Status
from db.enums import NotificationStatus


class NotificationResponse(BaseModel):
    id: uuid.UUID
    user_id: str
    message: str
    priority: Priority
    channels_requested: List[str]
    channel_used: Optional[str]
    status: NotificationStatus
    error_message: Optional[str]
    created_at: datetime
    sent_at: Optional[datetime]


    model_config = ConfigDict(from_attributes=True)


class NotificationCreateRequest(BaseModel):
    user_id: str
    message: str
    priority: Priority
    channels_requested: List[str]