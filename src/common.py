import logging
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class MoveCmd:
    domain: str
    source: int
    dest: int

@dataclass
class UnknownCmd:
    text: str

Command = MoveCmd | UnknownCmd

def log_function_call(logger: logging.Logger) -> Callable[..., Any]:
    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug(f'__Calling {f.__name__}')
            logger.debug(f'__Args: {" | ".join(str(x) for x in args)}')
            logger.debug(
                f'__Kwargs: {" | ".join(f"{k}: {v}" for k,v in kwargs.items())}')
            rv = f(*args, **kwargs)
            logger.debug(f'__Returning from {f.__name__}, result: {rv}')
            return rv
        return wrapper
    return decorator
