import uuid
from datetime import datetime, timezone

from db.session import async_session_factory, session_factory
from db.models.notification import NotificationsOrm, NotificationStatus


def insert_data():
    with session_factory() as session:
        notif_1 = NotificationsOrm(
            id=uuid.uuid4(),
            user_id="user_1",
            message="Welcome to our service!",
            channels_requested=["email"],
            channel_used=None,
            status=NotificationStatus.PENDING,
            error_message=None,
            created_at=datetime.now(timezone.utc),
            sent_at=None,
        )


        session.add_all([notif_1])
        session.commit()


async def insert_data_async():
    async with async_session_factory() as session:
        notif_1 = NotificationsOrm(
            id=uuid.uuid4(),
            user_id="user_1",
            message="Welcome to our service!",
            channels_requested=["email"],
            channel_used=None,
            status=NotificationStatus.PENDING,
            error_message=None,
            created_at=datetime.now(timezone.utc),
            sent_at=None,
        )

        notif_2 = NotificationsOrm(
            id=uuid.uuid4(),
            user_id="user_2",
            message="Your order has been shipped",
            channels_requested=["sms", "email"],
            channel_used="sms",
            status=NotificationStatus.SENT,
            error_message=None,
            created_at=datetime.now(timezone.utc),
            sent_at=datetime.now(timezone.utc),
        )

        notif_3 = NotificationsOrm(
            id=uuid.uuid4(),
            user_id="user_3",
            message="Payment failed",
            channels_requested=["sms"],
            channel_used="sms",
            status=NotificationStatus.FAILED,
            error_message="SMS provider error",
            created_at=datetime.now(timezone.utc),
            sent_at=None,
        )

        session.add_all([notif_1, notif_2, notif_3])
        await session.commit()