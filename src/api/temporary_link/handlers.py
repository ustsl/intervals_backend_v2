from typing import Optional
import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.temporary_link.actions import (
    _create_or_update_tmp_link,
    _get_dashboard_with_link,
)
from src.api.dashboard.actions.get import _get_dashboard, _get_dashboard_container
from src.api.account.actions import _get_account, _get_account_or_create
from src.api.auth.handlers import fastapi_users
from src.api.data.actions.get import _get_data_containers
from src.api.data.schemas import (
    PaginatedDataSchema,
)
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.post("/{dashboard_id}", status_code=201)
async def create_or_update_tmp_link(
    dashboard_id: str,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account_or_create(user_id=user.id, db=db)
    await _get_dashboard(dashboard_id=dashboard_id, account_id=account.id, db=db)
    result = await _create_or_update_tmp_link(dashboard_id=dashboard_id, db=db)
    return result


@router.get("/{secret_link}", status_code=200)
async def get_dashboard_view(
    secret_link: str,
    db: AsyncSession = Depends(get_db),
):
    dashboard = await _get_dashboard_with_link(secret_link=secret_link, db=db)
    return dashboard
