from fastapi import HTTPException
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.utils import forbid_account_key
from src.database.models.dashboard_model.dals import DashboardDAL
from src.database.models.dashboard_model.tables import DashboardModel


@forbid_account_key
async def _patch_dashboard_container(
    updates: dict, id: UUID, account_id: UUID, db: AsyncSession
):

    async with db as session:
        obj_dal = DashboardDAL(db_session=session, model=DashboardModel)
        result = await obj_dal.update(id=id, account=account_id, **updates)
        return result
