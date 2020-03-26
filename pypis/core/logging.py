import logging
import sys

from dynaconf import settings
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """Intercept standard logging messages toward Loguru sink."""
        logger_opt = logger.opt(depth=7, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def setup_logger() -> None:
    """Configure loguru logger."""
    L_LEVEL = logging.DEBUG if settings.LOGS.LEVEL == "debug" else logging.INFO
    logging.basicConfig(handlers=[InterceptHandler(level=L_LEVEL)], level=L_LEVEL)
    logger.configure(
        handlers=[{"sink": sys.stderr, "level": L_LEVEL}, {"sink": settings.LOGS.FILE}]
    )
