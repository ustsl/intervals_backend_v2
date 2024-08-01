from pydantic import BaseModel, model_validator


class PaginateSchemaMixin(BaseModel):
    total: int
    offset: int

    @model_validator(mode="after")
    def check_total(cls, values):
        total = values.total
        containers = values.containers
        if total < len(containers):
            raise ValueError("Total cannot be less than the number of containers")
        return values
