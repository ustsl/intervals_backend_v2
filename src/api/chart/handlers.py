from typing import Optional
import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account, _get_account_or_create
from src.api.auth.handlers import fastapi_users
from src.api.chart.actions.delete import _delete_chart_container
from src.api.chart.actions.get import _get_chart_container, _get_chart_containers
from src.api.chart.actions.patch import _patch_chart_container
from src.api.chart.actions.post import _create_chart_container
from src.api.chart.schemas import (
    ChartCreateSchema,
    ChartSchema,
    PaginateChartSchema,
    ChartFullGetSchema,
    ChartFullPostSchema,
)
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.post("/", status_code=201, response_model=ChartSchema)
async def create_chart_container(
    body: ChartCreateSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):

    account = await _get_account_or_create(user_id=user.id, db=db)
    chart_container = await _create_chart_container(
        title=body.title, account_id=account.id, db=db
    )
    return chart_container


@router.get("/", response_model=PaginateChartSchema, status_code=200)
async def get_chart_containers(
    offset: int = 0,
    title: Optional[str] = None,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    chart_containers = await _get_chart_containers(
        account_id=account.id, offset=offset, title=title, db=db
    )
    return chart_containers


@router.get("/{id}", response_model=ChartFullGetSchema, status_code=200)
async def get_chart_container(
    id: str, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)
    data_container = await _get_chart_container(id=id, account_id=account.id, db=db)
    return data_container


@router.patch("/{id}", status_code=201)
async def patch_data_container(
    id: str,
    updates: ChartFullPostSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    result = await _patch_chart_container(
        id=id, account_id=account.id, updates=updates, db=db
    )
    return result


@router.delete("/{id}", status_code=200)
async def delete_chart_container(
    id: str,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    delete = await _delete_chart_container(data_id=id, account_id=account.id, db=db)
    return delete
