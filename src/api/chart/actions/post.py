from sqlalchemy import UUID
from src.database.models.chart_model.tables import ChartModel
from src.database.models.data_model.dals import DataDAL
from src.api.chart.schemas import ChartPostSchema, ChartDataSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_chart_container(
    data: ChartDataSchema, account_id: UUID, db: AsyncSession
) -> ChartPostSchema:
    async with db as session:
        obj_dal = DataDAL(db_session=session, model=ChartModel)
        result = await obj_dal.create(
            title=data.title,
            settings=data.settings,
            account_id=account_id,
            data=data.data,
        )
        serialized_result = ChartPostSchema(
            id=result.id,
            title=result.title,
            time_update=result.time_update,
            data=result.data,
            settings=result.settings,
        )
        return serialized_result
