from sqlalchemy import event, inspect
from sqlalchemy.orm import Session

from db.enums import AuditOperation
from db.models.notification import NotificationsOrm
from observer_event_system.listeners.audit.audit_repository import AuditRepository


@event.listens_for(Session, "after_flush")
def audit_after_flush(session, flush_context):
    for obj in session.new:
        if isinstance(obj, NotificationsOrm):
            AuditRepository.log(
                entity='notifications',
                record_id=str(obj.id),
                operation=AuditOperation.INSERT,
            )

    for obj in session.deleted:
        if isinstance(obj, NotificationsOrm):
            AuditRepository.log(
                entity='notifications',
                record_id=str(obj.id),
                operation=AuditOperation.DELETE,
            )

    for obj in session.dirty:
        if isinstance(obj, NotificationsOrm):
            state = inspect(obj)
            if state.attrs.status.history.has_changes():
                AuditRepository.log(
                    entity='notifications',
                    record_id=str(obj.id),
                    operation=AuditOperation.UPDATE,
                )


