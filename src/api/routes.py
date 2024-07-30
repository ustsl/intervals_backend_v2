from fastapi.routing import APIRouter

from src.api.auth.handlers import router as auth_router
from src.api.account.handlers import router as account_router
from src.api.data.handlers import router as data_router
from src.api.chart.handlers import router as chart_router

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_api_router.include_router(account_router, prefix="/account", tags=["account"])
main_api_router.include_router(data_router, prefix="/data", tags=["data"])
main_api_router.include_router(chart_router, prefix="/chart", tags=["chart"])
