import uuid

from sqlalchemy import JSON, Boolean, Column, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins.base import TimeModel


class DataModel(Base, TimeModel):
    __tablename__ = "data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    account = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False)
    container = Column(JSON, nullable=True)
    info = Column(Text, nullable=True)
    is_open = Column(Boolean(), default=False, nullable=False)

    account_relation = relationship("AccountModel", back_populates="data_relation")
    chart_relation = relationship("ChartModel", back_populates="data_relation")
    widget_relation = relationship("WidgetModel", back_populates="data_relation")

    __table_args__ = (
        Index("ix_data_title", "title"),
        Index("ix_data_id_account", "id", "account"),
    )
