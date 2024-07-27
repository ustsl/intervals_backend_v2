from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import delete, desc, func, select, update
from src.database.utils import exception_dal, exception_soft_dal
from src.database.dals import BaseDAL

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class DataDAL(BaseDAL):

    @exception_dal
    async def delete(self, data_id: UUID, account_id: UUID):
        try:
            query = delete(self.model).where(
                self.model.id == data_id, self.model.account == account_id
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Obj deleted successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error deleting: {str(e)}"}

    @exception_dal
    async def update(self, data_id: UUID, account_id: UUID, **kwargs):
        try:
            update_values = {k: v for k, v in kwargs.items() if v is not None}
            query = (
                update(self.model)
                .where(self.model.id == data_id, self.model.account == account_id)
                .values(**update_values)
                .execution_options(synchronize_session="fetch")
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Updated successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error updating: {str(e)}"}

    async def create(self, title: str, container: dict, account_id: UUID):
        try:
            obj = self.model(title=title, container=container, account=account_id)
            self.db_session.add(obj)
            await self.db_session.flush()
            await self.db_session.commit()
            return obj
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"{e}")

    @exception_dal
    async def get(self, data_id: str, account_id: UUID):
        query = select(self.model).where(
            self.model.id == data_id, self.model.account == account_id
        )
        db_query_result = await self.db_session.execute(query)
        obj = db_query_result.scalar_one()
        return obj

    @exception_dal
    async def list(
        self,
        account_id: UUID,
        page_size: int = 10,
        offset: int = 0,
        order_param="time_update",
    ):
        query = (
            select(self.model)
            .where(self.model.account == account_id)
            .order_by(desc(getattr(self.model, order_param)))
            .limit(page_size)
            .offset(offset)
        )
        db_query_result = await self.db_session.execute(query)
        result = db_query_result.scalars().all()
        total_count_query = select(func.count()).select_from(self.model)
        total_count_result = await self.db_session.execute(total_count_query)
        total_count = total_count_result.scalar()
        return {"containers": result, "total": total_count, "offset": offset}
