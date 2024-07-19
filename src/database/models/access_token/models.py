from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from src.database.base import Base


class AccessTokenModel(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


async def get_access_token_db(
    session: AsyncSession,
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessTokenModel)
