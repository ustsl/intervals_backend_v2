from functools import wraps
from typing import Any, Awaitable, Callable

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound, SQLAlchemyError


def exception_dal(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Obj not found")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"{e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{e}")

    return wrapper


def exception_soft_dal(
    func: Callable[..., Awaitable[Any]]
) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            return {"status_code": 404}
        except SQLAlchemyError as e:
            return HTTPException(status_code=500, detail=f"{e}")
        except Exception as e:
            return HTTPException(status_code=500, detail=f"{e}")

    return wrapper


def forbid_account_key(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        updates = kwargs.get("updates", {})
        if "account" in updates:
            raise HTTPException(
                status_code=421, detail="Forbidden to pass 'account' in updates"
            )
        return await func(*args, **kwargs)

    return wrapper
