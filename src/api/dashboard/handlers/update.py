import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dashboard.actions.delete import (
    _force_delete_chart_to_dashboard,
    _force_delete_widget_to_dashboard,
)
from src.api.dashboard.actions.get import _get_dashboard_container
from src.api.dashboard.actions.post import (
    _relate_chart_to_dashboard,
    _relate_widget_to_dashboard,
)
from src.api.account.actions import _get_account
from src.api.auth.handlers import fastapi_users
from src.api.dashboard.actions.update import _patch_dashboard_container
from src.api.dashboard.schemas import DashboardSchema, DashboardPatchSchema
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.patch("/{id}", status_code=201)  # , response_model=DashboardSchema)
async def update_dashboard(
    id: str,
    updates: DashboardPatchSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):

    charts = updates.charts
    widgets = updates.widgets
    title = updates.title

    account = await _get_account(user_id=user.id, db=db)

    if title:
        await _patch_dashboard_container(
            id=id, account_id=account.id, title=updates.title, db=db
        )

    if widgets:
        await _force_delete_widget_to_dashboard(
            dashboard_id=id, account_id=account.id, db=db
        )
        for item in widgets:
            await _relate_widget_to_dashboard(
                object_id=item.object_id,
                dashboard_id=id,
                ordering=item.ordering,
                account_id=account.id,
                db=db,
            )

    if charts:
        await _force_delete_chart_to_dashboard(
            dashboard_id=id, account_id=account.id, db=db
        )
        for item in charts:
            await _relate_chart_to_dashboard(
                object_id=item.object_id,
                dashboard_id=id,
                ordering=item.ordering,
                account_id=account.id,
                db=db,
            )

    return {"success": "Updated successfully"}
