from typing import List

from interfaces.event_listener import EventListener
from observer_event_system.notification_event import NotificationEvent


class EventDispatcher:
    def __init__(self):
        self._listeners: list[EventListener] = []

    def attach(self, listener: EventListener):
        self._listeners.append(listener)

    def detach(self, listener: EventListener):
        self._listeners.remove(listener)

    def notify(self, event_data: NotificationEvent):
        for listener in self._listeners:
            listener.update(event_data)

