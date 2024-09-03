from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.api.schemas import PaginateSchemaMixin


class DashboardSchema(BaseModel):
    id: UUID
    account: UUID
    title: str
    time_update: datetime


class DashboardPostSchema(BaseModel):
    title: str


class DashboardChartSchema(BaseModel):
    chart_id: UUID


class DashboardWidgetSchema(BaseModel):
    widget_id: UUID


class DashboardDetailSchema(DashboardSchema):
    settings: object = None
    charts: Optional[List[DashboardChartSchema]] = None
    widgets: Optional[List[DashboardWidgetSchema]] = None


class PaginateDashboardSchema(PaginateSchemaMixin):
    containers: List[DashboardSchema]
