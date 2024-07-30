from fastapi import APIRouter, Depends
import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession


from src.api.chart.actions.post import _create_chart_container
from src.api.account.actions import _get_account, _get_account_or_create

from src.api.chart.schemas import ChartDataSchema
from src.database.session import get_db
from src.api.auth.handlers import fastapi_users

router = APIRouter()

current_user = fastapi_users.current_user()


@router.post("/", status_code=201)
async def post_chart_container(
    body: ChartDataSchema,
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):

    account = await _get_account_or_create(user_id=user.id, db=db)
    chart_container = await _create_chart_container(
        data=body, account_id=account.id, db=db
    )
    return chart_container
