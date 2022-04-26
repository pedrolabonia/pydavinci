from loguru import logger
import sys

logger.remove()


STR_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{file}</cyan>:<cyan>{line}</cyan> | <level>{message}</level> |"
)

logger.add(sink=sys.stderr, backtrace=True, format=STR_FORMAT)


def info(message: str):
    logger.opt(record=True, depth=2).info(message)


def warn(message: str) -> None:
    logger.opt(record=True, depth=2).warning(message)


def debug(message: str) -> None:
    logger.opt(record=True, depth=2).debug(message)


def error(message: str) -> None:
    logger.opt(depth=2).error(message)
