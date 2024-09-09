import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account_or_create
from src.api.auth.handlers import fastapi_users
from src.api.dashboard.actions.post import (_create_dashboard,
                                            _relate_chart_to_dashboard,
                                            _relate_widget_to_dashboard)
from src.api.dashboard.schemas import (DashboardPostSchema, DashboardSchema,
                                       RelationPostSchema)
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.post("/", status_code=201, response_model=DashboardSchema)
async def create_dashboard(
    body: DashboardPostSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account_or_create(user_id=user.id, db=db)
    dashboard_obj = await _create_dashboard(
        title=body.title, account_id=account.id, db=db
    )
    return dashboard_obj


@router.post("/chart_relation", status_code=201)
async def create_relation(
    body: RelationPostSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):

    account = await _get_account_or_create(user_id=user.id, db=db)
    dashboard_obj = await _relate_chart_to_dashboard(
        object_id=body.object_id,
        dashboard_id=body.dashboard_id,
        account_id=account.id,
        db=db,
    )
    return dashboard_obj


@router.post("/widget_relation", status_code=201)
async def create_relation(
    body: RelationPostSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account_or_create(user_id=user.id, db=db)
    dashboard_obj = await _relate_widget_to_dashboard(
        object_id=body.object_id,
        dashboard_id=body.dashboard_id,
        account_id=account.id,
        db=db,
    )
    return dashboard_obj
