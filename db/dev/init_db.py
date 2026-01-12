import uuid
from datetime import datetime, timezone

from db.session import sync_engine
from db.base import Base


def create_tables():
    Base.metadata.drop_all(sync_engine)
    sync_engine.echo = False
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True


