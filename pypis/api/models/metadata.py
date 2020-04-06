import re
from typing import Optional

from pydantic import ValidationError, validator

from pypis.api.models.base import BaseModel
from pypis.services.packages import is_valid_pep440_specifier


class BaseMetadata(BaseModel):
    version: str
    requires_python: Optional[str]

    @validator("version")
    def validate_version(cls, version: str) -> str:
        """Check version does not contains whitespaces."""
        version_re = re.compile(r"^(?!\s).*(?<!\s)$")
        if not version_re.match(version):
            raise ValidationError("Version Can't have leading or trailing whitespace.")
        return version

    @validator("requires_python")
    def validate_requires_python(cls, requires_python: str) -> str:
        """Check if requires_python is a valid pep440 version."""
        if not requires_python:
            return ""
        if not is_valid_pep440_specifier(requires_python):
            raise ValidationError("requires_python is not a valid pep 440 specifier")
        return requires_python
