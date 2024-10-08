from typing import Literal, Optional, Union
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dashboard.schemas import (DashboardChartSchema,
                                       DashboardDetailSchema)
from src.database.models.dashboard_model.dals import (DashboardDAL,
                                                      DashboardRelationDAL)
from src.database.models.dashboard_model.tables import (DashboardChart,
                                                        DashboardModel,
                                                        DashboardWidget)


async def _get_dashboard_containers(account_id: UUID, offset: int, db: AsyncSession):
    obj_dal = DashboardDAL(db_session=db, model=DashboardModel)
    obj = await obj_dal.list(account=account_id, offset=offset, page_size=5)
    return obj


async def _get_dashboard_container(id: str, account_id: UUID, db: AsyncSession):
    obj_dal = DashboardDAL(db_session=db, model=DashboardModel)
    obj = await obj_dal.get(id=id, account=account_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Dashboard not found")
    return obj


async def _get_dashboard_relation(
    dashboard_id: UUID,
    object_id: UUID,
    content: Literal["chart", "widget"],
    db: AsyncSession,
):
    if content == "chart":
        model = DashboardChart
    else:
        model = DashboardWidget

    obj_dal = DashboardRelationDAL(db_session=db, model=model)
    obj = await obj_dal.get(dashboard_id=dashboard_id, object_id=object_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Relation not found")
    return obj
