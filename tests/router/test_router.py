import uuid
from datetime import datetime, timezone

import pytest
from channels.email_channel import EmailChannel
from channels.settings import ChannelSettings
from channels.sms_channel import SMSChannel
from core.notification_channel import NotificationChannel
from core.notification_message import NotificationMessage, Priority
from core.notification_result import NotificationResult, Status
from core.notification_router import NotificationRouter, RouterConfig


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


def test_router_success(mocker, message):
    """Проверяет, что лишние каналы не вызываются"""
    sms_channel = mocker.Mock()
    email_channel = mocker.Mock()

    sms_channel.send.return_value = NotificationResult(
        status=Status.SENT,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )
    email_channel.send.return_value = NotificationResult(
        status=Status.SENT,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )

    channels = {
        "sms": sms_channel,
        "email": email_channel,
    }
    router_config = RouterConfig(
        channel_priority={
            Priority.LOW: ['sms', 'email'],
        },
        fallback_enabled=True,
    )

    router = NotificationRouter(
        channels=channels,
        config=router_config
    )

    message.channels_requested = ["email"]
    result = router.route(message)

    sms_channel.send.assert_not_called()
    email_channel.send.assert_called_once_with(message)

    assert result.status == Status.SENT
    assert result.channel_used == "email"


def test_router_failure(mocker, message):
    """Проверяет, что использован правильный channel_used"""
    sms_channel = mocker.Mock()
    email_channel = mocker.Mock()

    sms_channel.send.return_value = NotificationResult(
        status=Status.SENT,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )
    email_channel.send.return_value = NotificationResult(
        status=Status.SENT,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )

    channels = {
        "sms": sms_channel,
        "email": email_channel,
    }
    router_config = RouterConfig(
        channel_priority={
            Priority.LOW: ['sms', 'email'],
        },
        fallback_enabled=True,
    )

    router = NotificationRouter(
        channels=channels,
        config=router_config
    )

    message.channels_requested = ["sms", "email"]
    result = router.route(message)

    sms_channel.send.assert_called_once_with(message)
    email_channel.send.assert_not_called()

    assert result.status == Status.SENT
    assert result.channel_used == "sms"


def test_router_failure_1(mocker, message):
    """Первый канал падает → fallback включён => второй вызывается"""
    sms_channel = mocker.Mock()
    email_channel = mocker.Mock()

    sms_channel.send.return_value = NotificationResult(
        status=Status.FAILED,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )
    email_channel.send.return_value = NotificationResult(
        status=Status.SENT,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )

    channels = {
        "sms": sms_channel,
        "email": email_channel,
    }
    router_config = RouterConfig(
        channel_priority={
            Priority.LOW: ['sms', 'email'],
        },
        fallback_enabled=True,
    )

    router = NotificationRouter(
        channels=channels,
        config=router_config
    )

    message.channels_requested = ["sms", "email"]
    result = router.route(message)

    sms_channel.send.assert_called_once_with(message)
    email_channel.send.assert_called_once_with(message)

    assert result.status == Status.SENT
    assert result.channel_used == "email"


def test_router_failure_2(mocker, message):
    """Первый канал падает → fallback выключен => второй не вызывается"""
    sms_channel = mocker.Mock()
    email_channel = mocker.Mock()

    sms_channel.send.return_value = NotificationResult(
        status=Status.FAILED,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )
    email_channel.send.return_value = NotificationResult(
        status=Status.SENT,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )

    channels = {
        "sms": sms_channel,
        "email": email_channel,
    }
    router_config = RouterConfig(
        channel_priority={
            Priority.LOW: ['sms', 'email'],
        },
        fallback_enabled=False,
    )

    router = NotificationRouter(
        channels=channels,
        config=router_config
    )

    message.channels_requested = ["sms", "email"]
    result = router.route(message)

    sms_channel.send.assert_called_once_with(message)
    email_channel.send.assert_not_called()

    assert result.status == Status.FAILED
    assert result.channel_used == "sms"


def test_router_failure_3(mocker, message):
    """Все разрешенные каналы падают → failed"""
    sms_channel = mocker.Mock()
    email_channel = mocker.Mock()

    sms_channel.send.return_value = NotificationResult(
        status=Status.FAILED,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )
    email_channel.send.return_value = NotificationResult(
        status=Status.FAILED,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )

    channels = {
        "sms": sms_channel,
        "email": email_channel,
    }
    router_config = RouterConfig(
        channel_priority={
            Priority.LOW: ['sms', 'email'],
        },
        fallback_enabled=True,
    )

    router = NotificationRouter(
        channels=channels,
        config=router_config
    )

    message.channels_requested = ["sms", "email"]
    result = router.route(message)

    sms_channel.send.assert_called_once_with(message)
    email_channel.send.assert_called_once_with(message)

    assert result.status == Status.FAILED
    assert result.channel_used is None


def test_router_failure_4(mocker, message):
    """Нет пересечения priority и requested"""
    sms_channel = mocker.Mock()
    email_channel = mocker.Mock()

    sms_channel.send.return_value = NotificationResult(
        status=Status.FAILED,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )
    email_channel.send.return_value = NotificationResult(
        status=Status.FAILED,
        error_message=None,
        sent_at=datetime.now(timezone.utc),
        channel_used=None,
    )

    channels = {
        "sms": sms_channel,
        "email": email_channel,
    }
    router_config = RouterConfig(
        channel_priority={
            Priority.LOW: ['email'],
        },
        fallback_enabled=True,
    )

    router = NotificationRouter(
        channels=channels,
        config=router_config
    )

    message.channels_requested = ["sms"]
    result = router.route(message)

    sms_channel.send.assert_not_called()
    email_channel.send.assert_not_called()

    assert result.status == Status.FAILED
    assert result.channel_used is None