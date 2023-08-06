import asyncio
import logging
from contextlib import contextmanager
from typing import Any, Iterator, Tuple, Union

from attrs import Attribute
from attrs.validators import (
    ge,
    gt,
    instance_of,
)



def default_logger(logger: Union[logging.Logger, None]) -> logging.Logger:
    return logger or logging.getLogger(__name__)


def default_loop(
    loop: Union[asyncio.AbstractEventLoop, None]
) -> asyncio.AbstractEventLoop:
    return loop or asyncio.get_event_loop()


def ge_or_none(num: Union[int, float]) -> None:
    def _ge_or_none(inst: object, attr: Attribute, value: Any) -> None:
        if value is not None:
            ge(num)(inst, attr, value)
    return _ge_or_none


def gt_or_none(num: Union[int, float]) -> None:
    def _gt_or_none(inst: object, attr: Attribute, value: Any) -> None:
        if value is not None:
            gt(num)(inst, attr, value)
    return _gt_or_none


def instance_of_or_none(types: Union[Any, Tuple[Any]]) -> None:
    def _instance_of_or_none(inst: object, attr: Attribute, value: Any) -> None:
        if value is not None:
            instance_of(types)(inst, attr, value)
    return _instance_of_or_none


@contextmanager
def toggle_bool(inst: object, attr: str) -> Iterator[None]:
    try:
        if hasattr(inst, attr):
            setattr(inst, attr, False)
        yield
    finally:
        if hasattr(inst, attr):
            setattr(inst, attr, True)