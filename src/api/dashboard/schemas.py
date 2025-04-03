from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.api.chart.schemas import ChartFullGetSchema
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
    chart: ChartFullGetSchema


class DashboardWidgetSchema(BaseModel):
    object_id: UUID
    dashboard_id: UUID
    widget: FullWidgetSchema


class DashboardWidgetList(FullWidgetSchema):
    ordering: int


class DashboardChartList(ChartFullGetSchema):
    ordering: int


class DashboardDetailSchema(BaseModel):
    id: UUID
    title: str
    time_update: Optional[datetime] = None
    charts: Optional[List[DashboardChartList]] = None
    widgets: Optional[List[DashboardWidgetList]] = None

    model_config = ConfigDict(from_attributes=True)


class PaginateDashboardSchema(PaginateSchemaMixin):
    containers: List[DashboardSchema]


class RelationPostShortSchema(BaseModel):
    object_id: UUID
    ordering: int


class RelationPostSchema(RelationPostShortSchema):
    dashboard_id: UUID


class DashboardPatchSchema(BaseModel):
    title: str = None
    charts: Optional[List[RelationPostShortSchema]] = None
    widgets: Optional[List[RelationPostShortSchema]] = None
