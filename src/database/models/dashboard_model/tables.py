import uuid

from sqlalchemy import JSON, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from src.database.mixins.base import TimeModel
from src.database.base import Base


class DashboardModel(Base, TimeModel):
    __tablename__ = "dashboard"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    items = Column(JSON, nullable=False)
