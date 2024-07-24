from fastapi import APIRouter, Depends
import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account
from src.api.data.actions.post import _create_data_container
from src.api.data.schemas import PaginatedDataSchema, DataPostSchema
from src.database.session import get_db
from src.api.auth.handlers import fastapi_users

router = APIRouter()

current_user = fastapi_users.current_user()


@router.post("/", status_code=201)
async def post_data_container(
    body: DataPostSchema, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)
    data_container = await _create_data_container(
        data=body, account_id=account.id, db=db
    )
    return data_container


@router.get("/", response_model=PaginatedDataSchema, status_code=200)
async def get_data_containers(
    user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)

    return {"containers": [], "offset": 0, "total": 0}
