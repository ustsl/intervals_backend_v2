from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.widget_model.dals import WidgetDAL
from src.database.models.widget_model.tables import WidgetModel


async def _get_widget_containers(account_id: UUID, offset: int, db: AsyncSession):
    obj_dal = WidgetDAL(db_session=db, model=WidgetModel)
    obj = await obj_dal.list(account=account_id, offset=offset, page_size=5)
    return obj


async def _get_widget_container(id: str, account_id: UUID, db: AsyncSession):
    obj_dal = WidgetDAL(db_session=db, model=WidgetModel)
    obj = await obj_dal.get(id=id, account=account_id)
    return obj
