import uuid

from sqlalchemy import JSON, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins.base import TimeModel


class ChartModel(Base, TimeModel):
    __tablename__ = "chart"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    account = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False)
    data = Column(UUID(as_uuid=True), ForeignKey("data.id"), nullable=False)
    settings = Column(JSON, nullable=False)

    account_relation = relationship("AccountModel", back_populates="chart_relation")
    data_relation = relationship("DataModel", back_populates="chart_relation")
