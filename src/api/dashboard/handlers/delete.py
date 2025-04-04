import fastapi_users
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account
from src.api.auth.handlers import fastapi_users
from src.api.dashboard.actions.delete import (
    _delete_dashboard_container,
)

from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.delete("/{dashboard_id}", status_code=200)
async def delete_dashboard_container(
    dashboard_id: str,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    delete = await _delete_dashboard_container(
        id=dashboard_id, account_id=account.id, db=db
    )
    return delete
