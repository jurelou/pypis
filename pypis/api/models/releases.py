import re
from datetime import datetime
from typing import Optional, Any, Dict

from pydantic import (Schema,
                      ValidationError,
                      root_validator,
                      validator)

from pypis.api.models.base import EmailEmptyAllowedStr
from pypis.api.models.metadata import BaseMetadata


class BaseRelease(BaseMetadata):
    filename: str
    has_sig: bool = False
    comment_text: Optional[str]

    md5_digest: Optional[str]
    sha256_digest: Optional[str]
    blake2_256_digest: Optional[str]

    packagetype: str = Schema(None, alias="filetype")
    python_version: str = Schema(None, alias="pyversion")

    url: str = ""
    size: Optional[int]

    @validator("sha256_digest")
    def validate_sha256_digest(cls, sha256_digest: str) -> str:
        """Check if sha256_digest is a valid hex-encoded string."""
        if not sha256_digest:
            return ""
        sha256_re = re.compile(r"^[A-F0-9]{64}$", re.IGNORECASE)
        if not sha256_re.match(sha256_digest):
            raise ValidationError("sha256_digest is not a valid hex-encoded string.")
        return sha256_digest

    @validator("blake2_256_digest")
    def validate_blake2_256_digestt(cls, blake2_256_digest: str) -> str:
        """Check if blake2_256_digest is a valid hex-encoded string."""
        if not blake2_256_digest:
            return ""
        blake2_256_re = re.compile(r"^[A-F0-9]{64}$", re.IGNORECASE)
        if not blake2_256_re.match(blake2_256_digest):
            raise ValidationError("blake2_256_digest is not a valid hex-encoded string")
        return blake2_256_digest

    @root_validator
    def validate_all(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Check if packagetype and python_version are set."""
        values_cpy = values
        packagetype = values_cpy.get("packagetype", None)
        pyversion = values_cpy.get("python_version", None)

        if packagetype != "sdist" and not pyversion:
            raise ValueError(
                "Python version is required for binary distribution uploads."
            )

        if packagetype == "sdist":
            if not pyversion:
                values_cpy["python_version"] = "source"
            elif pyversion != "source":
                raise ValueError("Use 'source' as Python version for an sdist.")

        md5_digest = values_cpy.get("md5_digest", None)
        sha256_digest = values_cpy.get("sha256_digest", None)
        if not md5_digest and not sha256_digest:
            raise ValueError("Include at least one message digest.")

        return values_cpy


class ReleaseFromPypi(BaseRelease):
    upload_method: str = "pypi-proxy"

    upload_time: datetime
    upload_time_iso_8601: datetime


class ReleasePrivateUpload(BaseRelease):
    upload_method: str = "private-upload"

    keywords: Optional[str]
    platform: Optional[str]

    author: Optional[str]
    author_email: Optional[EmailEmptyAllowedStr]

    maintainer: Optional[str]
    maintainer_email: Optional[EmailEmptyAllowedStr]
