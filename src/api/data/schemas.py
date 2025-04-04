import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_validator

from src.api.schemas import PaginateSchemaMixin


class DataCreateSchema(BaseModel):
    title: str


class DataSchema(BaseModel):
    id: uuid.UUID
    title: str
    time_update: datetime


class FullDataSchema(DataSchema):
    time_create: datetime
    container: Optional[List[Dict[str, Any]]] = None
    info: Optional[str] = ""


class PaginatedDataSchema(PaginateSchemaMixin):
    containers: List[DataSchema]


class DataPatchSchema(BaseModel):
    title: str
    container: Dict[str, Any]
    info: Optional[str] = ""
