from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.api.chart.schemas import FullChartSchema
from src.api.data.schemas import FullDataSchema
from src.api.schemas import PaginateSchemaMixin
from src.api.widget.schemas import FullWidgetSchema


class DashboardSchema(BaseModel):
    id: UUID
    account: UUID
    title: str
    time_update: datetime


class DashboardPostSchema(BaseModel):
    title: str


class DashboardChartSchema(BaseModel):
    object_id: UUID
    dashboard_id: UUID
    chart: FullChartSchema


class DashboardWidgetSchema(BaseModel):
    object_id: UUID
    dashboard_id: UUID
    widget: FullWidgetSchema


class DashboardDetailSchema(DashboardSchema):
    settings: object = None
    charts: Optional[List[DashboardChartSchema]] = None
    widgets: Optional[List[DashboardWidgetSchema]] = None

    model_config = ConfigDict(from_attributes=True)


class PaginateDashboardSchema(PaginateSchemaMixin):
    containers: List[DashboardSchema]


class RelationPostSchema(BaseModel):
    dashboard_id: UUID
    object_id: UUID
