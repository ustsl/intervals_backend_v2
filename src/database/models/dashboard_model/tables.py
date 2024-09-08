import uuid

from sqlalchemy import JSON, CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins.base import TimeModel


class DashboardObjectMixin:
    order = Column(Integer, CheckConstraint("order > 0"), nullable=False, default=0)


class DashboardChart(Base, DashboardObjectMixin):
    __tablename__ = "dashboard_chart"

    dashboard_id = Column(
        UUID(as_uuid=True), ForeignKey("dashboard.id"), primary_key=True
    )
    object_id = Column(UUID(as_uuid=True), ForeignKey("chart.id"), primary_key=True)

    dashboard = relationship("DashboardModel", back_populates="charts")
    chart = relationship("ChartModel", back_populates="dashboard_charts")


class DashboardWidget(Base, DashboardObjectMixin):
    __tablename__ = "dashboard_widget"

    dashboard_id = Column(
        UUID(as_uuid=True), ForeignKey("dashboard.id"), primary_key=True
    )
    object_id = Column(UUID(as_uuid=True), ForeignKey("widget.id"), primary_key=True)

    dashboard = relationship("DashboardModel", back_populates="widgets")


class DashboardModel(Base, TimeModel):
    __tablename__ = "dashboard"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    settings = Column(JSON, nullable=True)
    account = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False)

    charts = relationship(
        "DashboardChart",
        back_populates="dashboard",
        cascade="all, delete-orphan",
    )
    widgets = relationship(
        "DashboardWidget",
        back_populates="dashboard",
        cascade="all, delete-orphan",
    )

    account_relation = relationship("AccountModel", back_populates="dashboard_relation")
