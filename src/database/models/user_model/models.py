from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from src.database.base import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession


class UserModel(SQLAlchemyBaseUserTableUUID, Base):
    pass


async def get_user_db(session: AsyncSession):
    yield SQLAlchemyUserDatabase(session, UserModel)
