import fastapi_users
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account, _get_account_or_create
from src.api.auth.handlers import fastapi_users
from src.api.widget.actions.delete import _delete_widget_container
from src.api.widget.actions.get import (_get_widget_container,
                                        _get_widget_containers)
from src.api.widget.actions.patch import _patch_widget_container
from src.api.widget.actions.post import _create_widget_container
from src.api.widget.schemas import (FullWidgetSchema, PaginateWidgetSchema,
                                    WidgetDataSchema)
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.post("/", status_code=201)
async def post_widget_container(
    body: WidgetDataSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account_or_create(user_id=user.id, db=db)
    widget_container = await _create_widget_container(
        data=body, account_id=account.id, db=db
    )
    return widget_container


@router.get("/", response_model=PaginateWidgetSchema, status_code=200)
async def get_widget_containers(
    offset: str = 0, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)
    widget_containers = await _get_widget_containers(
        account_id=account.id, offset=offset, db=db
    )
    return widget_containers


@router.get("/{id}", response_model=FullWidgetSchema, status_code=200)
async def get_widget_container(
    id: str, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)
    widget_container = await _get_widget_container(id=id, account_id=account.id, db=db)
    return widget_container


@router.patch("/{id}", status_code=200)
async def patch_widget_container(
    id: str,
    updates: dict,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    result = await _patch_widget_container(
        id=id, account_id=account.id, updates=updates, db=db
    )
    return result


@router.delete("/{id}", status_code=200)
async def delete_widget_container(
    id: str,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    delete = await _delete_widget_container(data_id=id, account_id=account.id, db=db)
    return delete
