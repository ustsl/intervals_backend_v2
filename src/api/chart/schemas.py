from typing import List, Union
import uuid

from pydantic import BaseModel, model_validator
from datetime import datetime


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


class ChartDataSchema(BaseModel):
    title: str
    data: uuid.UUID
    settings: dict


class ChartPostSchema(ChartSchema, ChartDataSchema):
    pass
