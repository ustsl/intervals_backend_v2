from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound

from src.database.models.chart_model.tables import ChartModel
from src.database.models.dashboard_model.tables import DashboardChart
from src.database.utils import exception_dal
from src.database.dals import AccountBaseDAL


class DashboardDAL(AccountBaseDAL):

    @exception_dal
    async def get(self, id: str, account: UUID):
        query = (
            select(self.model)
            .options(
                selectinload(self.model.charts).joinedload(DashboardChart.chart),
                selectinload(self.model.widgets),
            )
            .where(self.model.id == id, self.model.account == account)
        )
        db_query_result = await self.db_session.execute(query)

        try:
            return db_query_result.scalar_one()
        except NoResultFound:
            return None


class DashboardRelationDAL(AccountBaseDAL):
    pass
