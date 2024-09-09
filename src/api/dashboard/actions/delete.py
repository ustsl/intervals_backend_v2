from typing import Literal
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.chart.actions.get import _get_chart_container
from src.api.dashboard.actions.get import (
    _get_dashboard_relation,
)
from src.api.widget.actions.get import _get_widget_container
from src.database.models.dashboard_model.tables import (
    DashboardChart,
    DashboardWidget,
    DashboardModel,
)
from src.database.models.dashboard_model.dals import DashboardRelationDAL, DashboardDAL


async def _delete_dashboard_relation(
    dashboard_id: UUID,
    object_id: UUID,
    account_id: UUID,
    content: Literal["chart", "widget"],
    db: AsyncSession,
):

    await _get_dashboard_relation(
        dashboard_id=dashboard_id,
        object_id=object_id,
        content=content,
        db=db,
    )

    if content == "chart":
        await _get_chart_container(account_id=account_id, id=object_id, db=db)
        model = DashboardChart

    else:
        await _get_widget_container(account_id=account_id, id=object_id, db=db)
        model = DashboardWidget

    async with db as session:
        obj_dal = DashboardRelationDAL(db_session=session, model=model)
        result = await obj_dal.delete(dashboard_id=dashboard_id, object_id=object_id)
        return result


async def _delete_dashboard_container(id: UUID, account_id: UUID, db: AsyncSession):
    async with db as session:
        obj_dal = DashboardDAL(db_session=session, model=DashboardModel)
        result = await obj_dal.delete(id=id, account=account_id)
        return result
