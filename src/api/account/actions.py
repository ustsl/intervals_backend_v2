import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.account_model.dals import AccountDAL
from src.database.models.account_model.models import AccountModel


async def _create_account(user_id: uuid.UUID, db: AsyncSession):
    async with db as session:
        obj_dal = AccountDAL(db_session=session, model=AccountModel)
        result = await obj_dal.create(user_id=user_id)
        return result


async def _get_account_or_create(user_id: uuid.UUID, db: AsyncSession):

    obj_dal = AccountDAL(db_session=db, model=AccountModel)
    account = await obj_dal.get_with_user_id(user_id=user_id)
    if isinstance(account, dict) and account.get("status_code") == 404:
        return await _create_account(user_id=user_id, db=db)
    return account
