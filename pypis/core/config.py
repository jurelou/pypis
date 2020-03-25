from pypis.core.logging import setup_logger
from pypis.core.settings_validators import validate_settings


from pypis.services.proxy.pypi_proxy import PyPiProxy

def configure():
    validate_settings()
    setup_logger()

    PyPiProxy.configure()