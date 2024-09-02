from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.chart_model.dals import ChartDAL
from src.database.models.chart_model.tables import ChartModel


async def _patch_chart_container(
    updates: dict, id: UUID, account_id: UUID, db: AsyncSession
):
    async with db as session:
        obj_dal = ChartDAL(db_session=session, model=ChartModel)
        result = await obj_dal.update(id=id, account=account_id, **updates)
        return result
