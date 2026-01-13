import uuid
from datetime import datetime, timezone

import pytest

from channels.settings import ChannelSettings
from channels.sms_channel import SMSChannel
from core.notification_message import NotificationMessage, Priority
from core.notification_result import Status


@pytest.fixture
def message():
    """Provides a test message for the Notification System"""
    return NotificationMessage(
        id=uuid.uuid4(),
        user_id="test_user",
        message="Hello, world!",
        priority=Priority.LOW,
        channels_requested=["sms"],
        created_at=datetime.now(timezone.utc),
    )

def test_send_message_success(message, monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.99)
    settings = ChannelSettings(
        sms_enabled=True,
        sms_failure_rate=0.1,
    )
    sms_channel = SMSChannel(settings)
    result = sms_channel.send(message)

    assert result.status == Status.SENT
    assert result.error_message is None
    assert result.sent_at is not None

def test_send_message_failure(message, monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.1)
    settings = ChannelSettings(
        sms_enabled=True,
        sms_failure_rate=0.2,
    )
    sms_channel = SMSChannel(settings)
    result = sms_channel.send(message)

    assert result.status == Status.FAILED
    assert result.error_message == "SMS provider error"
    assert result.sent_at is None


def test_send_message_sms_not_enabled(message, monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.99)
    settings = ChannelSettings(
        sms_enabled=False,
        sms_failure_rate=0.1,
    )
    sms_channel = SMSChannel(settings)
    result = sms_channel.send(message)

    assert result.status == Status.FAILED
    assert result.error_message == "SMS channel is disabled by configuration"
    assert result.sent_at is None






