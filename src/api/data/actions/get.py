from sqlalchemy import UUID
from src.database.models.data_model.tables import DataModel
from src.database.models.data_model.dals import DataDAL
from src.api.account.actions import _get_account
from src.api.data.schemas import DataPostSchema, DataSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def _get_list_data_containers(
    account_id: UUID, offset: int, db: AsyncSession
) -> DataSchema:
    pass
