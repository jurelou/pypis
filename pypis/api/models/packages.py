import re
from typing import List, Optional, Union

from pydantic import (AnyHttpUrl,
                      Field,
                      ValidationError,
                      root_validator,
                      validator)

from pypis.api.models.base import BaseModel, EmailEmptyAllowedStr
from pypis.services.packages import is_valid_pep440_specifier, normalize_package_name


class PackageCreate(BaseModel):
    name: str
    classifiers: Optional[Union[List[str], str]]
    # keywords: Optional[str]

    license: Optional[str]

    version: str
    requires_python: Optional[str]
    # platform: Optional[str]

    author: str
    author_email: Optional[EmailEmptyAllowedStr]

    maintainer: Optional[str]
    maintainer_email: Optional[EmailEmptyAllowedStr]

    summary: Optional[str]
    description: Optional[str]
    description_content_type: Optional[str]

    home_page: Optional[str]
    package_url: Optional[str]
    project_url: Optional[str]
    bugtrack_url: Optional[str]
    docs_url: Optional[str]
    download_url: Optional[str]

    requires_dist: Optional[Union[str, List[str]]]

    @validator("requires_dist")
    def validate_requires_dist(cls, requires_dist: Union[str, List[str]]):
        if not requires_dist:
            return ""
        if not isinstance(requires_dist, list):
            requires_dist = [requires_dist]
        return "##".join(requires_dist)
    
        pass
    @validator("name")
    def validate_name(cls, name: str):
        name_re = re.compile(
            r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", re.IGNORECASE
        )
        assert name_re.match(
            name
        ), "Name should contains only letter, numeric, '.', '_', '-'"
        return normalize_package_name(name)

    @validator("version")
    def validate_version(cls, version: str):
        version_re = re.compile(r"^(?!\s).*(?<!\s)$")
        assert version_re.match(
            version
        ), "Version Can't have leading or trailing whitespace."
        return version

    @validator("summary")
    def validate_summary(cls, summary: str):
        summary_re = re.compile(r"^.+$")
        assert len(summary) <= 512, "Summary should be less than 512 chars."
        assert summary_re.match(summary), "Summary should contain one line only."
        return summary

    @validator("description_content_type")
    def validate_description_content_type(cls, description_content_type: str):
        if not description_content_type:
            return ""
        allowed_content_type = {"text/plain", "text/x-rst", "text/markdown"}
        assert (
            description_content_type in allowed_content_type
        ), "Invalid description_content_type"
        return description_content_type

    @validator("requires_python")
    def validate_requires_python(cls, requires_python: str):
        if not requires_python:
            return ""
        assert is_valid_pep440_specifier(
            requires_python
        ), "requires_python is not a valid pep 440 specifier"
        return requires_python


class PackageUpload(PackageCreate):
    metadata_version: str
    protocol_version: Optional[int]

    comment: Optional[str]


    @validator("protocol_version")
    def validate_protocol_version(cls, protocol_version: int):
        if not protocol_version:
            return protocol_version
        assert protocol_version == 1
        return protocol_version


    @validator("metadata_version")
    def validate_metadata_version(cls, metadata_version: str):
        allowed_metadata_versions = ("1.0", "1.1", "1.2", "2.0", "2.1")
        assert (
            metadata_version in allowed_metadata_versions
        ), "metadata_version not allowed."
        return metadata_version
