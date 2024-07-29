import uuid

from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.mixins.base import MaintenanceModel
from src.database.base import Base


class AccountModel(Base, MaintenanceModel):
    __tablename__ = "account"

    is_blocked = Column(Boolean(), default=False, nullable=False)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, unique=True
    )

    data_relation = relationship("DataModel", back_populates="account_relation")
    widget_relation = relationship("WidgetModel", back_populates="account_relation")
    chart_relation = relationship("ChartModel", back_populates="account_relation")
