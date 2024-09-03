from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.dashboard_model.dals import DashboardDAL
from src.database.models.dashboard_model.tables import DashboardModel


async def _get_dashboard_containers(account_id: UUID, offset: int, db: AsyncSession):
    obj_dal = DashboardDAL(db_session=db, model=DashboardModel)
    obj = await obj_dal.list(account=account_id, offset=offset, page_size=5)
    return obj


async def _get_dashboard_container(id: str, account_id: UUID, db: AsyncSession):
    obj_dal = DashboardDAL(db_session=db, model=DashboardModel)
    obj = await obj_dal.get(id=id, account=account_id)
    return obj
