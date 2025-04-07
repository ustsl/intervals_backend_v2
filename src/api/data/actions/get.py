from typing import Optional
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.data.schemas import DataSchema
from src.database.models.data_model.dals import DataDAL
from src.database.models.data_model.tables import DataModel


async def _get_data_container(id: str, account_id: UUID, db: AsyncSession):
    obj_dal = DataDAL(db_session=db, model=DataModel)
    obj = await obj_dal.get(id=id, account=account_id)
    return obj


async def _get_data_containers(
    account_id: UUID,
    offset: int,
    db: AsyncSession,
    title: Optional[str] = None,
) -> DataSchema:
    obj_dal = DataDAL(db_session=db, model=DataModel)

    obj = await obj_dal.list(
        account=account_id, offset=offset, page_size=50, title=title
    )
    return obj
