from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.widget_model.dals import WidgetDAL
from src.database.models.widget_model.tables import WidgetModel


async def _delete_widget_container(widget_id: UUID, account_id: UUID, db: AsyncSession):
    async with db as session:
        obj_dal = WidgetDAL(db_session=session, model=WidgetModel)
        result = await obj_dal.delete(id=widget_id, account=account_id)
        return result
