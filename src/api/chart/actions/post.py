from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.chart.schemas import ChartSchema
from src.database.models.chart_model.dals import ChartDAL
from src.database.models.chart_model.tables import ChartModel


async def _create_chart_container(title: str, account_id: UUID, db: AsyncSession):
    async with db as session:
        obj_dal = ChartDAL(db_session=session, model=ChartModel)
        result = await obj_dal.create(
            title=title,
            account=account_id,
        )
        serialized_result = ChartSchema(
            id=result.id,
            title=result.title,
            time_update=result.time_update,
        )
        return serialized_result
