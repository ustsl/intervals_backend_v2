from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.chart.actions.get import _get_chart_container
from src.api.dashboard.actions.get import _get_dashboard_container
from src.database.models.chart_model.dals import ChartDAL
from src.database.models.chart_model.tables import ChartModel
from src.api.dashboard.schemas import DashboardSchema
from src.database.models.dashboard_model.dals import DashboardDAL, DashboardRelationDAL
from src.database.models.dashboard_model.tables import (
    DashboardModel,
    DashboardChart,
    DashboardWidget,
)


async def _create_dashboard(title: str, account_id: UUID, db: AsyncSession):
    async with db as session:
        obj_dal = DashboardDAL(db_session=session, model=DashboardModel)
        result = await obj_dal.create(title=title, account=account_id)
        print(result)

        serialized_result = DashboardSchema(
            id=result.id,
            title=result.title,
            account=result.account,
            time_update=result.time_update,
        )
        return serialized_result


async def _relate_chart_to_dashboard(
    object_id: UUID, dashboard_id: UUID, account_id: UUID, db: AsyncSession
):
    await _get_chart_container(id=object_id, account_id=account_id, db=db)
    await _get_dashboard_container(id=dashboard_id, account_id=account_id, db=db)

    async with db as session:
        obj_dal = DashboardRelationDAL(db_session=session, model=DashboardChart)
        result = await obj_dal.create(dashboard_id=dashboard_id, object_id=object_id)
        return result
