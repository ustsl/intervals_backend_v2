from fastapi import APIRouter, Depends
import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.account.actions import _get_account_or_create
from src.api.account.schemas import AccountSchema

from src.database.session import get_db
from src.api.auth.handlers import fastapi_users

router = APIRouter()

current_user = fastapi_users.current_user()


@router.get("/")
async def get_account(
    user=Depends(current_user), db: AsyncSession = Depends(get_db)
):  # -> AccountSchema:

    result = await _get_account_or_create(user_id=user.id, db=db)

    return result


# @router.post("/", dependencies=[Depends(current_user)])
# async def create_account(
#     user_id: str, db: AsyncSession = Depends(get_db)
# ) -> UserRightsSchema:
#     return await _create_user_rights(user_id=user_id, db=db)


# @router.patch("/", dependencies=[Depends(current_user)])
# async def update_account(
#     user_id: int, updates: UserRightsExternalSchema, db: AsyncSession = Depends(get_db)
# ):
#     res = await _update_user_rights(user_id=user_id, updates=updates, db=db)
#     return res
