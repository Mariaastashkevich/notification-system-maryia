from api.app import create_app
import logging
import observer_event_system.listeners.audit.sqlalchemy_hooks

from logging_config import configure_logging


configure_logging(level=logging.INFO)
app = create_app()
