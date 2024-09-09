from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.database.utils import exception_dal
from src.database.dals import AccountBaseDAL

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class ChartDAL(AccountBaseDAL):
    @exception_dal
    async def get(self, id: UUID, account: UUID):
        query = (
            select(self.model)
            .options(selectinload(self.model.data_relation))
            .where(self.model.id == id, self.model.account == account)
        )
        db_query_result = await self.db_session.execute(query)
        obj = db_query_result.scalar_one()
        return obj
