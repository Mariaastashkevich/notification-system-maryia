import uuid
from datetime import datetime, timezone

import pytest

from core.notification_message import NotificationMessage, Priority
from core.notification_result import NotificationResult, Status
from notification_service import NotificationService


@pytest.fixture
def message():
    return NotificationMessage(
        id=uuid.uuid4(),
        user_id="test_user",
        message="Hello, world!",
        priority=Priority.LOW,
        channels_requested=["email", "sms"],
        created_at=datetime.now(timezone.utc),
    )

def test_success_notify(mocker, message):
    class FakeSession:
        def add(self, *args): pass

        def commit(self): pass

        def refresh(self, *args): pass

        def __enter__(self): return self

        def __exit__(self, *args): pass

    mocker.patch(
        "notification_service.get_session_factory",
        return_value=lambda: FakeSession(),
    )

    notification_router = mocker.Mock()
    event_dispatcher = mocker.Mock()

    notification_router.route.return_value = NotificationResult(
        status=Status.SENT,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used="email",
    )

    notification_service = NotificationService(
        notification_router,
        event_dispatcher
    )
    notification_service.send_notification(message)

    event_dispatcher.notify.assert_called_once()

    event = event_dispatcher.notify.call_args[0][0]
    assert event.status == Status.SENT
    assert event.channel == "email"
    assert event.notification_id == message.id


def test_failed_notify(mocker, message):
    class FakeSession:
        def add(self, *args): pass

        def commit(self): pass

        def refresh(self, *args): pass

        def __enter__(self): return self

        def __exit__(self, *args): pass

    mocker.patch(
        "notification_service.get_session_factory",
        return_value=lambda: FakeSession(),
    )

    notification_router = mocker.Mock()
    event_dispatcher = mocker.Mock()

    notification_router.route.return_value = NotificationResult(
        status=Status.FAILED,
        error_message="Email provider error",
        sent_at=None,
        channel_used="email",
    )

    notification_service = NotificationService(
        notification_router,
        event_dispatcher
    )
    notification_service.send_notification(message)

    event_dispatcher.notify.assert_called_once()

    event = event_dispatcher.notify.call_args[0][0]
    assert event.status == Status.FAILED
    assert event.channel == "email"
    assert event.notification_id == message.id


