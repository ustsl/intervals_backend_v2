from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy import delete, text
from sqlalchemy.future import select

from src.database.dals import AccountBaseDAL
from src.database.utils import exception_dal


class DashboardDAL(AccountBaseDAL):
    @exception_dal
    async def get_dashboard(
        self, dashboard_id: UUID, account_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        # Начинаем формирование запроса
        query = """
            SELECT id, title, time_update
            FROM dashboard
            WHERE id = :dashboard_id
        """
        params = {"dashboard_id": dashboard_id}

        # Если account_id передан, добавляем условие в запрос
        if account_id is not None:
            query += " AND account = :account"
            params["account"] = str(account_id)

        dashboard_sql = text(query)

        dashboard_result = await self.db_session.execute(dashboard_sql, params)
        dashboard_row = dashboard_result.fetchone()
        if not dashboard_row:
            return {}
        dashboard = dict(dashboard_row._mapping)
        return dashboard

    @exception_dal
    async def get_dashboard_charts(self, dashboard_id: str) -> Dict[str, Any]:
        charts_sql = text(
            """
            SELECT 
                c.id, 
                c.title, 
                c.data, 
                dt.time_update, 
                dt.container, 
                c.settings, 
                d.ordering
            FROM dashboard_chart AS d
            LEFT JOIN chart AS c ON c.id = d.object_id
            LEFT JOIN data AS dt ON c.data = dt.id
            WHERE d.dashboard_id = :dashboard_id
            ORDER BY d.ordering
        """
        )
        charts_result = await self.db_session.execute(
            charts_sql, {"dashboard_id": dashboard_id}
        )
        charts = [dict(row._mapping) for row in charts_result.fetchall()]
        return charts

    @exception_dal
    async def get_dashboard_widgets(self, dashboard_id: str) -> Dict[str, Any]:
        # Запрос для получения связанных виджетов
        widgets_sql = text(
            """
            SELECT 
                w.id, 
                w.title, 
                w.data, 
                dt.time_update, 
                dt.container, 
                d.ordering, 
                w.data_column, 
                w.offset_for_comparison, 
                w.account
            FROM dashboard_widget AS d
            LEFT JOIN widget AS w ON w.id = d.object_id
            LEFT JOIN data AS dt ON w.data = dt.id
            WHERE d.dashboard_id = :dashboard_id
            ORDER BY d.ordering
        """
        )
        widgets_result = await self.db_session.execute(
            widgets_sql, {"dashboard_id": dashboard_id}
        )
        widgets = [dict(row._mapping) for row in widgets_result.fetchall()]
        return widgets


class DashboardRelationDAL(AccountBaseDAL):
    @exception_dal
    async def change_or_create(self, dashboard_id, object_id, ordering):
        query = select(self.model).filter_by(
            dashboard_id=dashboard_id, object_id=object_id
        )
        result = await self.db_session.execute(query)
        instance = result.scalars().first()

        if instance:
            instance.ordering = ordering
        else:
            instance = self.model(
                dashboard_id=dashboard_id,
                object_id=object_id,
                ordering=ordering,
            )
            self.db_session.add(instance)

        await self.db_session.flush()
        await self.db_session.commit()
        return instance

    @exception_dal
    async def get(self, dashboard_id: UUID, object_id: UUID):
        query = select(self.model).where(
            self.model.dashboard_id == dashboard_id, self.model.object_id == object_id
        )
        db_query_result = await self.db_session.execute(query)
        obj = db_query_result.scalar_one()
        return obj

    @exception_dal
    async def force_delete(self, dashboard_id: UUID):
        try:
            query = delete(self.model).where(
                self.model.dashboard_id == dashboard_id,
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Obj deleted successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error deleting: {str(e)}"}

    @exception_dal
    async def delete(self, dashboard_id: UUID, object_id: UUID):
        try:
            query = delete(self.model).where(
                self.model.dashboard_id == dashboard_id,
                self.model.object_id == object_id,
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Obj deleted successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error deleting: {str(e)}"}
