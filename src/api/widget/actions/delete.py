from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession


async def _delete_widget_container(
    id: UUID, account_id: UUID, db: AsyncSession, objDAL, objModel
):
    async with db as session:
        obj_dal = objDAL(db_session=session, model=objModel)
        result = await obj_dal.delete(id=id, account=account_id)
        return result
