import logging
import sys
from dynaconf import settings
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        logger_opt = logger.opt(depth=7, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def setup_logger():
    LOGGING_LEVEL = logging.DEBUG if settings.LOG_LEVEL is "debug" else logging.INFO
    logging.basicConfig(
        handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
    )
    logger.configure(handlers=[
        {"sink": sys.stderr, "level": LOGGING_LEVEL},
        {"sink": settings.LOG_FILE}
        ])