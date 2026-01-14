from datetime import datetime, timezone
import uuid
from typing import Optional, Annotated

from sqlalchemy import Text, Enum, JSON

from core.notification_message import Priority
from db.enums import NotificationStatus
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[uuid.UUID, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime,
    mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc))
]
sent_at = Annotated[
    Optional[datetime],
    mapped_column(nullable=True)
]


class NotificationsOrm(Base): # определяем модель в декларативном стиле
    __tablename__ = "notifications"

    id: Mapped[intpk]
    user_id: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    channels_requested: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False
    )
    channel_used: Mapped[Optional[str]]
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus, name="notificationstatus"),
        nullable=False
    )

    priority: Mapped[Priority] = mapped_column(
        Enum(Priority),
        nullable=False
    )
    error_message: Mapped[Optional[str]]
    created_at: Mapped[created_at]
    sent_at: Mapped[sent_at]
