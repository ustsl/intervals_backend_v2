import uuid
from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from src.api.data.schemas import FullDataSchema
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
    title: str
    time_update: datetime


class ChartListSchema(ChartSchema):
    title: str


class ChartCreateSchema(BaseModel):
    title: str


class ChartDataSchema(BaseModel):
    title: str
    data: Optional[uuid.UUID]
    settings: Optional[dict]


class FullChartSchema(ChartDataSchema, ChartSchema):
    data_relation: Optional[FullDataSchema]


class ChartPostSchema(ChartSchema, ChartDataSchema):
    pass


class PaginateChartSchema(PaginateSchemaMixin):
    containers: List[ChartListSchema]
