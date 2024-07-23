import uuid

from sqlalchemy import Boolean, Column, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.mixins.base import MaintenanceModel, TimeModel
from src.database.base import Base


class DataModel(Base, MaintenanceModel, TimeModel):
    __tablename__ = "data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False)
    container = Column(JSON, nullable=False)
    is_open = Column(Boolean(), default=False, nullable=False)

    account = relationship("AccountModel", back_populates="data")
