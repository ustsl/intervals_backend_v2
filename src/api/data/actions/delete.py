from sqlalchemy import UUID
from src.database.models.data_model.tables import DataModel
from src.database.models.data_model.dals import DataDAL
from src.api.data.schemas import DataSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def _delete_data_container(id: UUID, account_id: UUID, db: AsyncSession):
    async with db as session:
        obj_dal = DataDAL(db_session=session, model=DataModel)
        result = await obj_dal.delete(id=id, account=account_id)
        return result
