from typing import List, Union
import uuid

from pydantic import BaseModel
from datetime import datetime

from src.api.schemas import PaginateSchemaMixin


class AxisYSchema(BaseModel):
    field: Union[str, int]
    type: str = None
    position: str = None
    color: str = None
    bg: str = None


class SettingsSchema(BaseModel):
    axisX: Union[str, int]
    axisY: List[AxisYSchema]


class ChartSchema(BaseModel):
    id: uuid.UUID
    time_update: datetime


class ChartListSchema(ChartSchema):
    title: str


class ChartDataSchema(BaseModel):
    title: str
    data: uuid.UUID
    settings: dict


class FullChartSchema(ChartDataSchema, ChartSchema):
    pass


class ChartPostSchema(ChartSchema, ChartDataSchema):
    pass


class PaginateChartSchema(PaginateSchemaMixin):
    containers: List[ChartListSchema]
