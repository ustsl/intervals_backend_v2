from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import (SQLAlchemyBaseUserTableUUID,
                              SQLAlchemyUserDatabase)
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import Base
from src.database.session import get_db


class UserModel(SQLAlchemyBaseUserTableUUID, Base):
    pass


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, UserModel)
