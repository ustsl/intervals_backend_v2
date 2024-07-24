from typing import Any, Dict, List
import uuid

from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime


class DataSchema(BaseModel):
    id: uuid.UUID
    title: str
    time_update: datetime


class PaginatedDataSchema(BaseModel):
    total: int
    offset: int
    containers: List[DataSchema]

    @model_validator(mode="after")
    def check_total(cls, values):
        total = values.total
        containers = values.containers
        if total < len(containers):
            raise ValueError("Total cannot be less than the number of containers")
        return values


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
