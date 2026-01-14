import uuid
from datetime import datetime, timezone

import pytest

from channels.email_channel import EmailChannel
from config.channels import ChannelSettings
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
        channels_requested=["email"],
        created_at=datetime.now(timezone.utc),
    )

def test_send_message_success(message, monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.99)
    settings = ChannelSettings(
        email_enabled=True,
        email_failure_rate=0.1,
    )
    email_channel = EmailChannel(settings)
    result = email_channel.send(message)

    assert result.status == Status.SENT
    assert result.error_message is None
    assert result.sent_at is not None

def test_send_message_failure(message, monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.1)
    settings = ChannelSettings(
        email_enabled=True,
        email_failure_rate=0.2,
    )
    email_channel = EmailChannel(settings)
    result = email_channel.send(message)

    assert result.status == Status.FAILED
    assert result.error_message == "Email provider error"
    assert result.sent_at is None


def test_send_message_email_not_enabled(message, monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.99)
    settings = ChannelSettings(
        email_enabled=False,
        email_failure_rate=0.1,
    )
    email_channel = EmailChannel(settings)
    result = email_channel.send(message)

    assert result.status == Status.FAILED
    assert result.error_message == "Email channel is disabled by configuration"
    assert result.sent_at is None






