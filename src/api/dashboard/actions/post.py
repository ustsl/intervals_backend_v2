from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dashboard.schemas import DashboardDetailSchema, DashboardSchema
from src.database.models.dashboard_model.dals import DashboardDAL
from src.database.models.dashboard_model.tables import DashboardModel


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
