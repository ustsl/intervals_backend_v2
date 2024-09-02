import uuid
from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

from src.api.schemas import PaginateSchemaMixin


class WidgetSchema(BaseModel):
    id: uuid.UUID
    time_update: datetime


class WidgetListSchema(WidgetSchema):
    title: str


class WidgetDataSchema(BaseModel):
    title: str
    data: uuid.UUID
    data_column: str
    offset_for_comparison: int


class FullWidgetSchema(WidgetDataSchema, WidgetSchema):
    pass


class WidgetPostSchema(WidgetSchema, WidgetDataSchema):
    pass


class PaginateWidgetSchema(PaginateSchemaMixin):
    containers: List[WidgetListSchema]
