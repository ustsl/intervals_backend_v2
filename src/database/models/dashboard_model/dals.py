from typing import Any, Dict
from uuid import UUID

from sqlalchemy import delete, text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.database.dals import AccountBaseDAL
from src.database.models.chart_model.tables import ChartModel
from src.database.models.dashboard_model.tables import DashboardChart, DashboardWidget
from src.database.models.widget_model.tables import WidgetModel
from src.database.utils import exception_dal

from sqlalchemy import text
from typing import Any, Dict
from uuid import UUID


class DashboardDAL(AccountBaseDAL):

    @exception_dal
    async def get(self, dashboard_id: str, account_id: UUID) -> Dict[str, Any]:
        # Запрос для получения информации по дашборду
        dashboard_sql = text(
            """
            SELECT id, title, time_update
            FROM dashboard
            WHERE id = :dashboard_id AND account = :account
        """
        )
        dashboard_result = await self.db_session.execute(
            dashboard_sql, {"dashboard_id": dashboard_id, "account": str(account_id)}
        )
        dashboard_row = dashboard_result.fetchone()
        if not dashboard_row:
            return {}  # Если дашборд не найден, возвращаем пустой словарь

        dashboard = dict(dashboard_row._mapping)

        # Запрос для получения связанных чартов
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
            charts_sql, {"dashboard_id": dashboard_id, "account": str(account_id)}
        )
        charts = [dict(row._mapping) for row in charts_result.fetchall()]

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
            WHERE d.dashboard_id = :dashboard_id AND w.account = :account
            ORDER BY d.ordering
        """
        )
        widgets_result = await self.db_session.execute(
            widgets_sql, {"dashboard_id": dashboard_id, "account": str(account_id)}
        )
        widgets = [dict(row._mapping) for row in widgets_result.fetchall()]

        # Формируем итоговый словарь с результатами
        result = {
            **dashboard,
            "charts": charts,
            "widgets": widgets,
        }
        return result


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
