from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account
from src.api.data.schemas import DataPostSchema, DataSchema
from src.database.models.data_model.dals import DataDAL
from src.database.models.data_model.tables import DataModel


async def _create_data_container(
    data: DataPostSchema, account_id: UUID, db: AsyncSession
) -> DataSchema:
    async with db as session:
        obj_dal = DataDAL(db_session=session, model=DataModel)
        result = await obj_dal.create(
            title=data.title, container=data.container, account=account_id
        )
        serialized_result = DataSchema(
            id=result.id, title=result.title, time_update=result.time_update
        )
        return serialized_result
