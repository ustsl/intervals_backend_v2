from typing import Optional
import uuid

from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: uuid.UUID
    is_active: bool
    is_blocked: bool
