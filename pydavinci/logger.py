import sys
from typing import Any

from loguru import logger

logger.remove()


STR_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{module}</cyan>:<cyan>{line}</cyan> | <level>{message}</level> |"
)

logger.add(sink=sys.stderr, backtrace=True, format=STR_FORMAT, level="INFO")


def info(message: str, depth: int = 2) -> None:
    return logger.opt(record=True, depth=depth).info(message)


def warn(message: str, depth: int = 2) -> None:
    return logger.opt(record=True, depth=depth).warning(message)


def debug(message: str, depth: int = 2) -> None:
    return logger.opt(record=True, depth=depth).debug(message)


def error(message: str, depth: int = 2) -> None:
    return logger.opt(depth=depth).error(message)


def raise_exception(exception: Any, message: str, depth: int = 2) -> None:
    try:
        raise exception
    except exception:
        return logger.opt(exception=exception, depth=depth).info(message)
