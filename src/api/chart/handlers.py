from fastapi import APIRouter, Depends
import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession


from src.api.chart.actions.get import _get_chart_containers, _get_chart_container
from src.api.chart.actions.post import _create_chart_container
from src.api.account.actions import _get_account, _get_account_or_create

from src.api.chart.schemas import ChartDataSchema, FullChartSchema, PaginateChartSchema
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


@router.get("/", response_model=PaginateChartSchema, status_code=200)
async def get_chart_containers(
    offset: str = 0, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)
    data_containers = await _get_chart_containers(
        account_id=account.id, offset=offset, db=db
    )

    return data_containers


@router.get("/{chart_id}", response_model=FullChartSchema, status_code=200)
async def get_chart_container(
    chart_id: str, user=Depends(current_user), db: AsyncSession = Depends(get_db)
):
    account = await _get_account(user_id=user.id, db=db)
    data_container = await _get_chart_container(
        chart_id=chart_id, account_id=account.id, db=db
    )
    return data_container
