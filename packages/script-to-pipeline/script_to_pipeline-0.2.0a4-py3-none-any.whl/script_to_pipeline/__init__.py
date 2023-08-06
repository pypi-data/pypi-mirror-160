import os
from functools import partial, wraps
from inspect import getfullargspec
from pathlib import Path
from typing import Callable, Dict, Optional

from .constants import ENTRYPOINT_ATTR, PIPELINE_INPUT_ATTR, PIPELINE_NAME_ATTR
from .pfs import PFS
from .utils import create_test_datum, in_container

__all__ = ("pipeline", "PFS")


def pipeline(
    pipeline_function: Optional[Callable] = None,
    *,
    name: Optional[str] = None,
    input: Optional["PFS"] = None
):
    def set_attributes(func):
        setattr(func, ENTRYPOINT_ATTR, True)
        setattr(func, PIPELINE_NAME_ATTR, name)
        setattr(func, PIPELINE_INPUT_ATTR, input)

    if not in_container():
        # If we aren't running in the container, pass through
        if not pipeline_function:
            return partial(pipeline, name=name, input=input)
        set_attributes(pipeline_function)
        setattr(pipeline_function, "test_datum", create_test_datum(pipeline_function, input))
        return pipeline_function

    def pipeline_decorator(pipeline_function_inner):
        @wraps(pipeline_function_inner)
        def wrapped_function(*args, **kwargs):
            signature = getfullargspec(pipeline_function_inner)
            if "out" in signature.args:
                kwargs["out"] = Path("/pfs/out")
            if "datum" in signature.args:
                kwargs["datum"] = Path(os.getenv(input.repo))
            return pipeline_function_inner(*args, **kwargs)
        set_attributes(wrapped_function)

        setattr(pipeline_function_inner, "test_datum", lambda *_, **__: None)
        return wrapped_function

    if pipeline_function:
        return pipeline_decorator(pipeline_function)
    return pipeline_decorator
