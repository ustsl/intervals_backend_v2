from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from src.database.utils import exception_dal, exception_soft_dal
from src.database.dals import BaseDAL

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class DataDAL(BaseDAL):

    # @exception_soft_dal
    # async def get_with_user_id(self, user_id: int):
    #     query = select(self.model).where(self.model.user == user_id)
    #     db_query_result = await self.db_session.execute(query)
    #     obj = db_query_result.scalar_one()
    #     return obj

    async def create(self, title: str, container: dict, account_id: UUID):
        try:
            obj = self.model(title=title, container=container, account=account_id)
            self.db_session.add(obj)
            await self.db_session.flush()
            await self.db_session.commit()
            return obj
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"{e}")
