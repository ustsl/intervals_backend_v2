from fastapi.routing import APIRouter

from src.api.auth.handlers import router as auth_router
from src.api.account.handlers import router as account_router


# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_api_router.include_router(account_router, prefix="/account", tags=["account"])
