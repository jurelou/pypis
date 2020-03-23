from pypis.core.settings_validators import validate_settings
from pypis.core.logging import setup_logger

def configure():
    validate_settings()
    setup_logger()
    