from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.widget.schemas import WidgetDataSchema, WidgetPostSchema, WidgetSchema
from src.database.models.widget_model.dals import WidgetDAL
from src.database.models.widget_model.tables import WidgetModel


async def _create_widget_container(
    title: str, account_id: UUID, db: AsyncSession
) -> WidgetPostSchema:
    async with db as session:
        obj_dal = WidgetDAL(db_session=session, model=WidgetModel)
        result = await obj_dal.create(
            title=title,
            account=account_id,
        )
        serialized_result = WidgetSchema(
            id=result.id,
            title=result.title,
            time_update=result.time_update,
        )
        return serialized_result
