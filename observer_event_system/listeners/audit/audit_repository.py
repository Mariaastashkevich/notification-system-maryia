from db.enums import AuditOperation
from db.models.audit_trail import AuditTrailOrm
from db.session import session_factory


class AuditRepository:
    @staticmethod
    def log(entity: str, record_id: str | None, operation: AuditOperation):
        with session_factory() as session:
            session.add(
                AuditTrailOrm(
                    entity=entity,
                    record_id=record_id,
                    operation=operation.value,
                )
            )
            session.commit()







