import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from api.deps import get_notification_service
from api.schemas.notification import NotificationResponse
from core.notification_message import NotificationMessage, Priority
from db.enums import NotificationStatus
from main import app


@pytest.fixture
def message():
    return NotificationMessage(
        id=uuid.uuid4(),
        user_id="example_user",
        message="Hello, world!",
        priority=Priority.NORMAL,
        channels_requested=["sms", "email"],
        created_at=datetime.now(timezone.utc),
    )


class FakeNotificationService:
    def __init__(self):
        self._notification = None

    def send_notification(self, message: NotificationMessage) -> NotificationResponse:
        notification = NotificationResponse(
            id=message.id,
            user_id=message.user_id,
            message=message.message,
            priority=message.priority,
            channels_requested=message.channels_requested,
            channel_used="sms",
            status=NotificationStatus.SENT,
            error_message=None,
            created_at=message.created_at,
            sent_at=datetime.now(timezone.utc),
            )
        self._notification = notification
        return notification

    def get_notification(self, notification_id: uuid.UUID) -> NotificationResponse | None:
        if self._notification is not None:
            if self._notification.id == notification_id:
                return self._notification
        return None


@pytest.fixture
def client():
    fake_service = FakeNotificationService()
    app.dependency_overrides[get_notification_service] = lambda: fake_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_send_notification_success(client, message):
    response = client.post(
        "/notifications/notify",
        json={
            "user_id": message.user_id,
            "message": message.message,
            "priority": message.priority.value,
            "channels_requested": message.channels_requested,
        }
    )

    assert response.status_code == 200
    body = response.json()

    assert body['channel_used'] == "sms"
    assert body['status'] == NotificationStatus.SENT
    assert body['error_message'] is None
    assert body['user_id'] == message.user_id
    assert "id" in body
    assert "created_at" in body


def test_get_notification_success(client, message):
    post_response = client.post(
        "/notifications/notify",
        json={
            "user_id": message.user_id,
            "message": message.message,
            "priority": message.priority.value,
            "channels_requested": message.channels_requested,
        }
    )

    notification_id = post_response.json()['id']

    response = client.get(
        f"/notifications/{notification_id}",
    )

    assert response.status_code == 200

    body = response.json()
    assert body['channels_requested'] == message.channels_requested
    assert body['message'] == message.message
    assert body['priority'] == message.priority.value
    assert body['user_id'] == message.user_id
    assert body['status'] == NotificationStatus.SENT.value


