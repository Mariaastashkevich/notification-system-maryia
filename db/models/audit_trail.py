from datetime import datetime, timezone
import uuid
from typing import Annotated

from sqlalchemy import String, Integer, DateTime
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[uuid.UUID, mapped_column(primary_key=True, default=uuid.uuid4)]
created_at = Annotated[
    datetime,
    mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
]


class AuditTrailOrm(Base): # определяем модель в декларативном стиле
    __tablename__ = "audit_trail"

    id: Mapped[intpk]
    entity: Mapped[str] = mapped_column(String, nullable=False)
    operation: Mapped[str] = mapped_column(String, nullable=False)
    record_id: Mapped[str | None]
    record_count: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[created_at]

