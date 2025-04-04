from typing import Optional

import fastapi_users
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account, _get_account_or_create
from src.api.auth.handlers import fastapi_users
from src.api.data.actions.delete import _delete_data_container
from src.api.data.actions.get import _get_data_container, _get_data_containers
from src.api.data.actions.patch import _patch_data_container
from src.api.data.actions.post import _create_data_container
from src.api.data.schemas import (
    DataCreateSchema,
    DataPatchSchema,
    DataSchema,
    FullDataSchema,
    PaginatedDataSchema,
)
from src.database.session import get_db

router = APIRouter()

current_user = fastapi_users.current_user()


@router.get("/", response_model=PaginatedDataSchema, status_code=200)
async def get_data_containers(
    offset: int = 0,
    title: Optional[str] = None,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    data_containers = await _get_data_containers(
        account_id=account.id, offset=offset, title=title, db=db
    )
    return data_containers


@router.get("/{data_id}", response_model=FullDataSchema, status_code=200)
async def get_data_container(
    data_id: str, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)
    data_container = await _get_data_container(id=data_id, account_id=account.id, db=db)
    if not data_container:
        raise HTTPException(status_code=404, detail=f"Data not found")
    return data_container


@router.post("/", status_code=201, response_model=DataSchema)
async def post_data_container(
    body: DataCreateSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account_or_create(user_id=user.id, db=db)
    data_container = await _create_data_container(
        title=body.title, account_id=account.id, db=db
    )
    return data_container


@router.patch("/{data_id}", status_code=201)
async def patch_data_container(
    data_id: str,
    updates: DataPatchSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    result = await _patch_data_container(
        id=data_id, account_id=account.id, updates=updates, db=db
    )
    return result


@router.delete("/{data_id}", status_code=200)
async def delete_data_container(
    data_id: str,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await _get_account(user_id=user.id, db=db)
    delete = await _delete_data_container(id=data_id, account_id=account.id, db=db)
    return delete
