from typing import Literal
import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dashboard.actions.delete import (
    _delete_dashboard_container,
    _delete_dashboard_relation,
)
from src.api.account.actions import _get_account, _get_account_or_create
from src.api.auth.handlers import fastapi_users
from src.api.dashboard.actions.post import _create_dashboard, _relate_chart_to_dashboard
from src.api.dashboard.schemas import (
    ChartRelationPostSchema,
    DashboardPostSchema,
    DashboardSchema,
)
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.delete("/{content}/{dashboard_id}/{object_id}", status_code=200)
async def delete_dashboard_chart_relation(
    content: Literal["chart", "widget"],
    dashboard_id: str,
    object_id: str,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):

    account = await _get_account(user_id=user.id, db=db)
    result = await _delete_dashboard_relation(
        dashboard_id=dashboard_id,
        object_id=object_id,
        account_id=account.id,
        content=content,
        db=db,
    )
    return result


@router.delete("/{id}", status_code=200)
async def delete_dashboard_container(
    id: str,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    delete = await _delete_dashboard_container(id=id, account_id=account.id, db=db)
    return delete
