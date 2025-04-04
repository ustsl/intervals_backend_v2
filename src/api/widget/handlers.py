from typing import Optional

import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account, _get_account_or_create
from src.api.auth.handlers import fastapi_users
from src.api.widget.actions.delete import _delete_widget_container
from src.api.widget.actions.get import _get_widget_container, _get_widget_containers
from src.api.widget.actions.patch import _patch_widget_container
from src.api.widget.actions.post import _create_widget_container
from src.api.widget.schemas import (
    FullWidgetSchema,
    PaginateWidgetSchema,
    WidgetDataSchema,
    WidgetSchema,
    WidgetSchemaCreate,
)
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.post("/", status_code=201, response_model=WidgetSchema)
async def post_widget_container(
    body: WidgetSchemaCreate,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account_or_create(user_id=user.id, db=db)
    widget_container = await _create_widget_container(
        title=body.title, account_id=account.id, db=db
    )
    return widget_container


@router.get("/", response_model=PaginateWidgetSchema, status_code=200)
async def get_widget_containers(
    offset: int = 0,
    title: Optional[str] = None,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    widget_containers = await _get_widget_containers(
        account_id=account.id, offset=offset, title=title, db=db
    )
    return widget_containers


@router.get("/{widget_id}", response_model=FullWidgetSchema, status_code=200)
async def get_widget_container(
    widget_id: str, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)
    widget_container = await _get_widget_container(
        id=widget_id, account_id=account.id, db=db
    )
    return widget_container


@router.patch("/{widget_id}", status_code=201)
async def patch_widget_container(
    widget_id: str,
    updates: dict,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    result = await _patch_widget_container(
        id=widget_id, account_id=account.id, updates=updates, db=db
    )
    return result


@router.delete("/{widget_id}", status_code=200)
async def delete_widget_container(
    id: str,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    delete = await _delete_widget_container(data_id=id, account_id=account.id, db=db)
    return delete
