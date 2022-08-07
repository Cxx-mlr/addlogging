from typing import TypeVar, ParamSpec, overload
from collections.abc import Awaitable, Callable
import functools
import logging

P = ParamSpec("P")
R = TypeVar("R")

logger = logging.getLogger(__name__)

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("file.log")
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

c_format = logging.Formatter("%(levelname)-7s - %(module)s.%(funcName)s: %(message)s")
f_format = logging.Formatter("%(asctime)s - %(levelname)-7s - %(module)s.%(funcName)s: %(message)s")
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

logger.setLevel(logging.INFO)
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.propagate = False

@overload
def addlogging(func_: Callable[P, R], *, logger: logging.Logger = ...) -> Callable[P, R | None]: ...

@overload
def addlogging(func_: None=None, *, logger: logging.Logger = ...) -> Callable[[Callable[P, R]], Callable[P, R | None]]: ...

def addlogging(func_: Callable[P, R] | None = None, *, logger: logging.Logger = logger) -> Callable[P, R | None] | Callable[[Callable[P, R]], Callable[P, R | None]]:
    def decorator_add_logging(func: Callable[P, R]) -> Callable[P, R | None]:
        @functools.wraps(func)
        def wrapper_addlogging(*args: P.args, **kwargs: P.kwargs) -> R | None:
            args_repr: tuple[str, ...] = tuple(repr(a) for a in args)
            kwargs_repr: tuple[str, ...] = tuple(f"{k}={v!r}" for k, v in kwargs.items())
            signature: str = ", ".join(args_repr + kwargs_repr)
            logger.info(f"calling {func.__name__}({signature})")
            try:
                result: R = func(*args, **kwargs)
            except Exception as e:
                logger.exception(str(e))
                return None
            else:
                logger.info(f"{func.__name__!r} returned {result!r}")
                return result
        return wrapper_addlogging
    if func_ is None:
        return decorator_add_logging
    else:
        return decorator_add_logging(func_)

@overload
def async_addlogging(func_: Callable[P, Awaitable[R]], *, logger: logging.Logger = ...) -> Callable[P, Awaitable[R | None]]: ...

@overload
def async_addlogging(func_: None=None, *, logger: logging.Logger = ...) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R | None]]]: ...

def async_addlogging(func_: Callable[P, Awaitable[R]] | None = None, *, logger: logging.Logger = logger) -> Callable[P, Awaitable[R | None]] | Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R | None]]]:
    def decorator_async_addlogging(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
        @functools.wraps(func)
        async def wrapper_addlogging(*args: P.args, **kwargs: P.kwargs) -> R | None:
            args_repr: tuple[str, ...] = tuple(repr(a) for a in args)
            kwargs_repr: tuple[str, ...] = tuple(f"{k}={v!r}" for k, v in kwargs.items())
            signature: str = ", ".join(args_repr + kwargs_repr)
            logger.info(f"Calling {func.__name__}({signature})")
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                logger.exception(str(e))
                return None
            else:
                logger.info(f"{func.__name__!r} returned {result!r}")
                return result
        return wrapper_addlogging
    if func_ is None:
        return decorator_async_addlogging
    else:
        return decorator_async_addlogging(func_)
