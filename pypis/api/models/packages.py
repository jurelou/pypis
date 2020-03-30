import re
from typing import List, Optional, Union

from pydantic import ValidationError, validator

from pypis.api.models.metadata import BaseMetadata
from pypis.services.packages import normalize_package_name
from pypis.api.models.base import EmailEmptyAllowedStr


class PackageCreate(BaseMetadata):
    name: str
    summary: Optional[str]
    classifiers: Optional[Union[List[str], str]]

    license: Optional[str]

    description: Optional[str]
    description_content_type: Optional[str]

    home_page: Optional[str]
    package_url: Optional[str]
    project_url: Optional[str]
    bugtrack_url: Optional[str]
    docs_url: Optional[str]
    download_url: Optional[str]

    requires_dist: Optional[Union[str, List[str]]]

    author: str
    author_email: Optional[EmailEmptyAllowedStr]

    maintainer: Optional[str]
    maintainer_email: Optional[EmailEmptyAllowedStr]

    @validator("summary")
    def validate_summary(cls, summary: str) -> str:
        """Check if summary is a valid one line string."""
        summary_re = re.compile(r"^.+$")
        if len(summary) > 512:
            raise ValidationError("Summary should be less than 512 chars.")

        if not summary_re.match(summary):
            raise ValidationError("Summary should contain one line only.")
        return summary

    @validator("requires_dist")
    def validate_requires_dist(cls, requires_dist: Union[str, List[str]]) -> str:
        """Translate a list of requires to a string using ## as a separator."""
        if not requires_dist:
            return ""
        if not isinstance(requires_dist, list):
            requires_dist = [requires_dist]
        return "##".join(requires_dist)

        pass

    @validator("name")
    def validate_name(cls, name: str) -> str:
        """Normalize the project name."""
        name_re = re.compile(
            r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", re.IGNORECASE
        )
        if not name_re.match(name):
            raise ValidationError("Name should contains only letter, \
                numeric, '.', '_', '-'")
        return normalize_package_name(name)

    @validator("description_content_type")
    def validate_description_content_type(cls, description_content_type: str) -> str:
        """Check if description_content_type is a known format."""
        if not description_content_type:
            return ""
        allowed_content_type = {"text/plain", "text/x-rst", "text/markdown"}
        if description_content_type not in allowed_content_type:
            raise ValidationError("Invalid description_content_type")
        return description_content_type


class PackageUpload(PackageCreate):
    metadata_version: str
    protocol_version: Optional[int]

    comment: Optional[str]

    @validator("protocol_version")
    def validate_protocol_version(cls, protocol_version: int) -> int:
        """Check if protocol_version is 1."""
        if not protocol_version:
            return protocol_version
        if protocol_version != 1:
            raise ValidationError("Protocol version 1 only supported.")
        return protocol_version

    @validator("metadata_version")
    def validate_metadata_version(cls, metadata_version: str) -> str:
        """Check if metadata_version is known."""
        allowed_metadata_versions = ("1.0", "1.1", "1.2", "2.0", "2.1")
        if metadata_version not in allowed_metadata_versions:
            raise ValidationError("metadata_version not allowed.")
        return metadata_version
