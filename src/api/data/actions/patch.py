from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.data.schemas import DataSchema
from src.database.models.data_model.dals import DataDAL
from src.database.models.data_model.tables import DataModel


async def _patch_data_container(
    updates: dict, id: UUID, account_id: UUID, db: AsyncSession
):
    async with db as session:
        obj_dal = DataDAL(db_session=session, model=DataModel)
        result = await obj_dal.update(id=id, account=account_id, **updates)
        return result
