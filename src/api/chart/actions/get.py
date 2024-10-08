from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.chart_model.dals import ChartDAL
from src.database.models.chart_model.tables import ChartModel


async def _get_chart_containers(account_id: UUID, offset: int, db: AsyncSession):
    obj_dal = ChartDAL(db_session=db, model=ChartModel)
    obj = await obj_dal.list(account=account_id, offset=offset, page_size=5)
    return obj


async def _get_chart_container(id: str, account_id: UUID, db: AsyncSession):
    obj_dal = ChartDAL(db_session=db, model=ChartModel)
    obj = await obj_dal.get(id=id, account=account_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Chart not found")
    return obj
