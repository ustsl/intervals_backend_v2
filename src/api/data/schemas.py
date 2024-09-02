import uuid
from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, field_validator

from src.api.schemas import PaginateSchemaMixin


class DataSchema(BaseModel):
    id: uuid.UUID
    title: str
    time_update: datetime


class FullDataSchema(DataSchema):
    time_create: datetime
    container: Dict[str, Any]


class PaginatedDataSchema(PaginateSchemaMixin):
    containers: List[DataSchema]


class DataPostSchema(BaseModel):
    title: str
    container: Dict[str, Any]

    @field_validator("container")
    def check_container(cls, value):
        if "data" not in value or not isinstance(value["data"], str):
            raise ValueError('container must have a key "data" with a string value')
        return value


class DataPostSchema(BaseModel):
    title: str
    container: Dict[str, Any]

    @field_validator("container")
    def check_container(cls, value):
        if "data" not in value or not isinstance(value["data"], str):
            raise ValueError('container must have a key "data" with a string value')
        return value
