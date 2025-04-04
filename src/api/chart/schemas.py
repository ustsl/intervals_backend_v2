import uuid
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from src.api.data.schemas import FullDataSchema
from src.api.schemas import PaginateSchemaMixin


class AxisYSchema(BaseModel):
    field: str
    side: Literal["left", "right"]
    type: Literal["bar", "line", "area"]


class ChartCreateSchema(BaseModel):
    title: str


class ChartSchema(ChartCreateSchema):
    id: uuid.UUID
    time_update: Optional[datetime] = None


class PaginateChartSchema(PaginateSchemaMixin):
    containers: List[ChartSchema]


class ChartSettingsSchema(BaseModel):
    axisX: Optional[str] = None
    axisY: Optional[List[AxisYSchema]] = None


class ChartFullPostSchema(ChartCreateSchema):
    data: Optional[uuid.UUID] = None
    settings: Optional[ChartSettingsSchema] = None

    class Config:
        extra = "forbid"


class ChartFullGetSchema(ChartFullPostSchema, ChartSchema):
    container: Optional[List[Dict[str, Any]]] = None
    info: Optional[str] = ""
