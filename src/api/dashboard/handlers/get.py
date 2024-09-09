import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account, _get_account_or_create
from src.api.auth.handlers import fastapi_users
from src.api.dashboard.actions.get import (_get_dashboard_container,
                                           _get_dashboard_containers)
from src.api.dashboard.schemas import (DashboardDetailSchema,
                                       PaginateDashboardSchema)
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.get("/", response_model=PaginateDashboardSchema, status_code=200)
async def get_dashboards(
    offset: str = 0, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account_or_create(user_id=user.id, db=db)
    data_containers = await _get_dashboard_containers(
        account_id=account.id, offset=offset, db=db
    )
    return data_containers


@router.get("/{id}", response_model=DashboardDetailSchema, status_code=200)
async def get_dashboard(
    id: str, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)
    dashboard = await _get_dashboard_container(id=id, account_id=account.id, db=db)
    return dashboard
