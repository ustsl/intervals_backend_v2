from sqlalchemy import UUID, select, text
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.database.dals import AccountBaseDAL
from src.database.utils import exception_dal

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class WidgetDAL(AccountBaseDAL):
    @exception_dal
    async def get(self, id: UUID, account: UUID):
        sql = text(
            """
            SELECT 
                c.id, c.title, c.data, c.data_column, c.offset_for_comparison, c.time_update, dt.container
            FROM widget AS c
            LEFT JOIN data AS dt ON dt.id = c.data
            WHERE c.account = :account AND c.id = :id
        """
        )

        result = await self.db_session.execute(
            sql, {"account": str(account), "id": str(id)}
        )
        row = result.mappings().one()
        return dict(row)
