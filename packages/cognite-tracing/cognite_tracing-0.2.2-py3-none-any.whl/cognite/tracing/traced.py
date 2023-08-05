import inspect
from functools import wraps
from inspect import getattr_static
from typing import Any, Callable, Dict, List, TypeVar, cast

from cognite.tracing import span

T = TypeVar("T", bound=Callable)


def traced(f: T) -> T:
    """Decorator for enabling tracing of this function"""
    if inspect.iscoroutinefunction(f):

        @wraps(f)
        async def decorated(*args: List, **kwargs: Dict) -> Any:
            with span(name=f.__qualname__):
                result = await f(*args, **kwargs)
                return result

    else:

        @wraps(f)
        def decorated(*args: List, **kwargs: Dict) -> Any:
            with span(name=f.__qualname__):
                result = f(*args, **kwargs)
                return result

    return cast(T, decorated)


def traced_methods(cls: T) -> T:
    """Decorator for enabling tracing of all public instance methods within the class"""
    for attr in cls.__dict__:
        attr_is_public_method = not attr.startswith("_") and callable(getattr(cls, attr))
        attr_is_staticmethod = isinstance(getattr_static(cls, attr), staticmethod)
        attr_is_classmethod = isinstance(getattr_static(cls, attr), classmethod)
        if attr_is_public_method and not attr_is_staticmethod and not attr_is_classmethod:
            setattr(cls, attr, traced(getattr(cls, attr)))
    return cls
