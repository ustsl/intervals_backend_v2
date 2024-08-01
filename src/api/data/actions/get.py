from sqlalchemy import UUID
from src.database.models.data_model.tables import DataModel
from src.database.models.data_model.dals import DataDAL
from src.api.account.actions import _get_account
from src.api.data.schemas import DataPostSchema, DataSchema, PaginatedDataSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def _get_data_container(
    data_id: str, account_id: UUID, db: AsyncSession
) -> DataSchema:
    obj_dal = DataDAL(db_session=db, model=DataModel)
    obj = await obj_dal.get(id=data_id, account=account_id)
    return obj


async def _get_data_containers(
    account_id: UUID, offset: int, db: AsyncSession
) -> DataSchema:
    obj_dal = DataDAL(db_session=db, model=DataModel)
    obj = await obj_dal.list(account=account_id, offset=offset, page_size=5)
    return obj
