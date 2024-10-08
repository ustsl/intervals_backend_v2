from fastapi import HTTPException
from sqlalchemy import select

from src.database.dals import BaseDAL
from src.database.utils import exception_dal, exception_soft_dal

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class AccountDAL(BaseDAL):

    @exception_soft_dal
    async def get_with_user_id(self, user_id: int):
        query = select(self.model).where(self.model.user == user_id)
        db_query_result = await self.db_session.execute(query)
        obj = db_query_result.scalar_one()
        return obj

    async def create(self, user_id):
        try:
            obj = self.model(user=user_id)
            self.db_session.add(obj)
            await self.db_session.flush()
            await self.db_session.commit()
            return obj
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"{e}")
