from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import delete, desc, func, select, update
from src.database.utils import exception_dal, exception_soft_dal
from src.database.dals import BaseDAL

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class ChartDAL(BaseDAL):

    async def create(self, title: str, data: UUID, settings: dict):
        try:
            obj = self.model(title=title, data=data, settings=settings)
            self.db_session.add(obj)
            await self.db_session.flush()
            await self.db_session.commit()
            return obj
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"{e}")
