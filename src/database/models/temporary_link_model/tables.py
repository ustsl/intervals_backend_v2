import uuid

from datetime import datetime, timedelta
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


from src.database.base import Base


class TemporaryLinkModel(Base):
    __tablename__ = "temporary_link"

    id = Column(UUID(as_uuid=True), ForeignKey("dashboard.id"), primary_key=True)
    secret_link = Column(UUID(as_uuid=True), default=uuid.uuid4)
    available_until = Column(
        DateTime, default=lambda: datetime.now() + timedelta(days=1)
    )
