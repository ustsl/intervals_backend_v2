from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta

from src.database.utils import exception_dal

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class BaseDAL:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model

    @exception_dal
    async def create(self, **data):
        try:
            obj = self.model(**data)
            self.db_session.add(obj)
            await self.db_session.flush()
            return obj
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"{e}")

    @exception_dal
    async def list(self, page_size: int = 10, offset: int = 0, order_param="id"):
        query = (
            select(self.model)
            .order_by(desc(getattr(self.model, order_param)))
            .limit(page_size)
            .offset(offset)
        )
        db_query_result = await self.db_session.execute(query)
        result = db_query_result.scalars().all()
        total_count_query = select(func.count()).select_from(self.model)
        total_count_result = await self.db_session.execute(total_count_query)
        total_count = total_count_result.scalar()
        return {"result": result, "total": total_count}

    @exception_dal
    async def get(self, id: int):
        query = select(self.model).where(self.model.id == id)
        db_query_result = await self.db_session.execute(query)
        obj = db_query_result.scalar_one()
        return obj

    @exception_dal
    async def update(self, id, **kwargs):
        try:
            update_values = {k: v for k, v in kwargs.items() if v is not None}
            query = (
                update(self.model)
                .where(self.model.id == id)
                .values(**update_values)
                .execution_options(synchronize_session="fetch")
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Updated successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error updating: {str(e)}"}

    @exception_dal
    async def delete(self, id: UUID):
        try:
            query = delete(self.model).where(self.model.id == id)
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Obj deleted successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error deleting: {str(e)}"}

    @exception_dal
    async def safe_delete(self, id: UUID):
        try:
            query = (
                update(self.model).where(self.model.id == id).values(is_deleted=True)
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Obj deleted successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error deleting obj: {str(e)}"}

    @exception_dal
    async def update(self, id: UUID, **kwargs):
        try:
            update_values = {k: v for k, v in kwargs.items() if v is not None}

            query = (
                update(self.model)
                .where(self.model.id == id)
                .values(**update_values)
                .execution_options(synchronize_session="fetch")
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Updated successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error updating: {str(e)}"}


class AccountBaseDAL(BaseDAL):

    async def create(self, **kwargs):
        try:
            obj = self.model(**kwargs)
            self.db_session.add(obj)
            await self.db_session.flush()
            await self.db_session.commit()
            return obj
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"{e}")

    @exception_dal
    async def get(self, id: str, account: UUID):
        query = select(self.model).where(
            self.model.id == id, self.model.account == account
        )
        db_query_result = await self.db_session.execute(query)
        obj = db_query_result.scalar_one()
        return obj

    @exception_dal
    async def list(
        self,
        account: UUID,
        page_size: int = 10,
        offset: int = 0,
        order_param="time_update",
    ):
        query = (
            select(self.model)
            .where(self.model.account == account)
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

    @exception_dal
    async def delete(self, id: UUID, account: UUID):
        try:
            query = delete(self.model).where(
                self.model.id == id, self.model.account == account
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Obj deleted successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error deleting: {str(e)}"}

    @exception_dal
    async def update(self, id: UUID, account: UUID, **kwargs):
        try:
            update_values = {k: v for k, v in kwargs.items() if v is not None}
            query = (
                update(self.model)
                .where(self.model.id == id, self.model.account == account)
                .values(**update_values)
                .execution_options(synchronize_session="fetch")
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Updated successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error updating: {str(e)}"}
