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
