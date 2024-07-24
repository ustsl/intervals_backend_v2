import uuid

from fastapi import APIRouter


from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from src.api.auth.manager import get_user_manager
from src.api.auth.schemas import UserCreate, UserRead
from src.api.auth.strategy import auth_backend
from src.database.models.user_model.tables import UserModel

fastapi_users = FastAPIUsers[UserModel, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="",
    tags=["auth"],
)
