from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.data.schemas import DataSchema
from src.database.models.data_model.dals import DataDAL
from src.database.models.data_model.tables import DataModel


async def _create_data_container(
    title: str, account_id: UUID, db: AsyncSession
) -> DataSchema:
    async with db as session:
        obj_dal = DataDAL(db_session=session, model=DataModel)
        result = await obj_dal.create(title=title, account=account_id)
        serialized_result = DataSchema(
            id=result.id, title=result.title, time_update=result.time_update
        )
        return serialized_result
