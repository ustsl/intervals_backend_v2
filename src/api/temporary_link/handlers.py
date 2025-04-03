from uuid import UUID
import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dashboard.schemas import DashboardDetailSchema
from src.api.account.actions import _get_account_or_create
from src.api.auth.handlers import fastapi_users
from src.api.dashboard.actions.get import _get_dashboard
from src.api.temporary_link.actions import (
    _create_or_update_tmp_link,
    _get_dashboard_with_link,
)
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.post("/{dashboard_id}", status_code=201)
async def create_or_update_tmp_link(
    dashboard_id: UUID,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account_or_create(user_id=user.id, db=db)
    await _get_dashboard(dashboard_id=dashboard_id, account_id=account.id, db=db)
    result = await _create_or_update_tmp_link(dashboard_id=dashboard_id, db=db)
    return result


@router.get("/{secret_link}", status_code=200, response_model=DashboardDetailSchema)
async def get_dashboard_view(
    secret_link: UUID,
    db: AsyncSession = Depends(get_db),
):
    dashboard = await _get_dashboard_with_link(secret_link=secret_link, db=db)
    return dashboard
