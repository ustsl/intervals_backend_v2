from sqlalchemy import UUID
from src.database.models.widget_model.dals import WidgetDAL
from src.database.models.widget_model.tables import WidgetModel
from src.api.widget.schemas import WidgetPostSchema, WidgetDataSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_widget_container(
    data: WidgetDataSchema, account_id: UUID, db: AsyncSession
) -> WidgetPostSchema:
    async with db as session:
        obj_dal = WidgetDAL(db_session=session, model=WidgetModel)
        result = await obj_dal.create(
            title=data.title,
            account=account_id,
            data=data.data,
            data_column=data.data_column,
            offset_for_comparison=data.offset_for_comparison,
        )
        serialized_result = WidgetPostSchema(
            id=result.id,
            title=result.title,
            time_update=result.time_update,
            data=result.data,
            offset_for_comparison=result.offset_for_comparison,
            data_column=result.data_column,
        )
        return serialized_result
