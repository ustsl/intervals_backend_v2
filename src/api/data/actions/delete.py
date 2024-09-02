from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.data.schemas import DataSchema
from src.database.models.data_model.dals import DataDAL
from src.database.models.data_model.tables import DataModel


async def _delete_data_container(id: UUID, account_id: UUID, db: AsyncSession):
    async with db as session:
        obj_dal = DataDAL(db_session=session, model=DataModel)
        result = await obj_dal.delete(id=id, account=account_id)
        return result
