from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.dashboard_model.dals import DashboardDAL
from src.database.models.dashboard_model.tables import DashboardModel
from src.database.models.temporary_link_model.dals import TemporaryLinkDAL
from src.database.models.temporary_link_model.tables import TemporaryLinkModel


async def _create_or_update_tmp_link(dashboard_id: UUID, db: AsyncSession):
    async with db as session:
        obj_dal = TemporaryLinkDAL(db_session=session, model=TemporaryLinkModel)
        result = await obj_dal.create_or_update(dashboard_id=dashboard_id)
        return result


async def _get_dashboard_with_link(secret_link: UUID, db: AsyncSession):
    secret_link_dal = TemporaryLinkDAL(db_session=db, model=TemporaryLinkModel)
    dashboard_object = await secret_link_dal.get(secret_link=secret_link)
    obj_dal = DashboardDAL(db_session=db, model=DashboardModel)
    dashboard = await obj_dal.get_dashboard(dashboard_id=dashboard_object.get("id"))
    charts = await obj_dal.get_dashboard_charts(dashboard_id=dashboard.get("id"))
    widgets = await obj_dal.get_dashboard_widgets(dashboard_id=dashboard.get("id"))
    result = {
        **dashboard,
        "charts": charts,
        "widgets": widgets,
    }

    return result
    return obj
