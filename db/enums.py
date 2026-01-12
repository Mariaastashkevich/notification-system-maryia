import enum


class NotificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

class AuditOperation(enum.Enum):
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'

