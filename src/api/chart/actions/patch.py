from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.utils import forbid_account_key
from src.api.data.actions.get import _get_data_container
from src.database.models.chart_model.dals import ChartDAL
from src.database.models.chart_model.tables import ChartModel


@forbid_account_key
async def _patch_chart_container(
    updates: dict, id: UUID, account_id: UUID, db: AsyncSession
):
    if updates.get("data"):
        await _get_data_container(id=updates.get("data"), account_id=account_id, db=db)
    async with db as session:
        obj_dal = ChartDAL(db_session=session, model=ChartModel)
        result = await obj_dal.update(id=id, account=account_id, **updates)
        return result
