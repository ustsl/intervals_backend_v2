from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.chart_model.dals import ChartDAL
from src.database.models.chart_model.tables import ChartModel


async def _delete_chart_container(chart_id: UUID, account_id: UUID, db: AsyncSession):
    async with db as session:
        obj_dal = ChartDAL(db_session=session, model=ChartModel)
        result = await obj_dal.delete(id=chart_id, account=account_id)
        return result
