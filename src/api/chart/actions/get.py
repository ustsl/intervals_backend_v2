from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.chart_model.dals import ChartDAL
from src.database.models.chart_model.tables import ChartModel


async def _get_chart_containers(account_id: UUID, offset: int, db: AsyncSession):
    obj_dal = ChartDAL(db_session=db, model=ChartModel)
    obj = await obj_dal.list(account=account_id, offset=offset, page_size=5)
    return obj


async def _get_chart_container(chart_id: str, account_id: UUID, db: AsyncSession):
    obj_dal = ChartDAL(db_session=db, model=ChartModel)
    obj = await obj_dal.get(id=chart_id, account=account_id)
    return obj
