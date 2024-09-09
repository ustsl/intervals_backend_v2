import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account
from src.api.auth.handlers import fastapi_users
from src.api.dashboard.actions.update import _patch_dashboard_container
from src.api.dashboard.schemas import DashboardSchema
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.patch("/", status_code=201, response_model=DashboardSchema)
async def update_dashboard(
    id: str,
    updates: dict,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    result = await _patch_dashboard_container(
        id=id, account_id=account.id, updates=updates, db=db
    )
    return result
