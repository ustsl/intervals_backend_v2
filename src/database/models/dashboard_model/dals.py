from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.database.dals import AccountBaseDAL
from src.database.models.chart_model.tables import ChartModel
from src.database.models.dashboard_model.tables import (DashboardChart,
                                                        DashboardWidget)
from src.database.models.widget_model.tables import WidgetModel
from src.database.utils import exception_dal


class DashboardDAL(AccountBaseDAL):

    @exception_dal
    async def get(self, id: str, account: UUID):
        query = (
            select(self.model)
            .options(
                selectinload(self.model.charts)
                .joinedload(DashboardChart.chart)
                .joinedload(ChartModel.data_relation),
                selectinload(self.model.widgets)
                .joinedload(DashboardWidget.widget)
                .joinedload(WidgetModel.data_relation),
            )
            .where(self.model.id == id, self.model.account == account)
        )
        db_query_result = await self.db_session.execute(query)

        try:
            return db_query_result.scalar_one()
        except NoResultFound:
            return None


class DashboardRelationDAL(AccountBaseDAL):

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
