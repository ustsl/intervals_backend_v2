from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.utils import forbid_account_key
from src.api.data.actions.get import _get_data_container
from src.database.models.widget_model.dals import WidgetDAL
from src.database.models.widget_model.tables import WidgetModel


@forbid_account_key
async def _patch_widget_container(
    updates: dict, id: UUID, account_id: UUID, db: AsyncSession
):
    if updates.get("data"):
        await _get_data_container(id=updates.get("data"), account_id=account_id, db=db)
    async with db as session:
        obj_dal = WidgetDAL(db_session=session, model=WidgetModel)
        result = await obj_dal.update(id=id, account=account_id, **updates)
        return result
