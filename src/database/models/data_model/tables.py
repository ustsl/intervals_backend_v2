import uuid

from sqlalchemy import Boolean, Column, ForeignKey, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.mixins.base import MaintenanceModel, TimeModel
from src.database.base import Base


class DataModel(Base, TimeModel):
    __tablename__ = "data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    account = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False)
    container = Column(JSON, nullable=False)
    is_open = Column(Boolean(), default=False, nullable=False)

    account_relation = relationship("AccountModel", back_populates="data_relation")
