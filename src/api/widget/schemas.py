import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from src.api.data.schemas import FullDataSchema
from src.api.schemas import PaginateSchemaMixin


class WidgetSchemaCreate(BaseModel):
    title: str


class WidgetSchema(BaseModel):
    id: uuid.UUID
    title: str
    time_update: Optional[datetime] = None


class WidgetListSchema(WidgetSchema):
    title: str


class WidgetDataSchema(BaseModel):
    title: str
    data: Optional[uuid.UUID] = None
    data_column: Optional[str] = None
    offset_for_comparison: Optional[int] = None


class FullWidgetSchema(WidgetDataSchema, WidgetSchema):
    container: Optional[List[Dict[str, Any]]] = None
    info: Optional[str] = ""


class WidgetPostSchema(WidgetSchema, WidgetDataSchema):
    pass


class PaginateWidgetSchema(PaginateSchemaMixin):
    containers: List[WidgetListSchema]
