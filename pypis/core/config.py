from dynaconf import settings

from pypis.core.logging import setup_logger
from pypis.core.settings_validators import validate_settings
from pypis.services.proxy.pypi_proxy import PyPiProxy


def configure() -> None:
    """Configure the application (logging, settings, PyPi proxy)."""
    validate_settings()
    setup_logger()
    PyPiProxy.configure(settings.PYPI_PROXY.PYPI_URL)
