import re
from datetime import datetime
from typing import List, Optional, Union

from pypis.api.models.base import BaseModel
from pypis.services.packages import canonicalize_package_version



from pydantic import (AnyHttpUrl,
                      Field,
                      ValidationError,
                      root_validator,
                      Schema,
                      validator)

from pypis.api.models.base import BaseModel, EmailEmptyAllowedStr
from pypis.services.packages import is_valid_pep440_specifier, normalize_package_name




class ReleaseCreate(BaseModel):
    version: str
    # comment_text: str
    filename: str

    has_sig: bool
    comment_text: Optional[str]
    md5_digest: Optional[str]
    sha256_digest: Optional[str]
    blake2_256_digest: Optional[str]

    packagetype: str
    python_version: str
    requires_python: Optional[str]

    size: int
    upload_time: datetime
    upload_time_iso_8601: datetime
    url: str
    

    @validator("version")
    def validate_version(cls, version: str):
        return canonicalize_package_version(version)

    @validator("sha256_digest")
    def validate_md5_digest(cls, sha256_digest: str):
        if not sha256_digest:
            return ""
        sha256_re = re.compile(r"^[A-F0-9]{64}$", re.IGNORECASE)
        assert sha256_re.match(
            sha256_digest
        ), "sha256_digest is not a valid hex-encoded string."
        return sha256_digest

    @validator("blake2_256_digest")
    def validate_blake2_256_digestt(cls, blake2_256_digest: str):
        if not blake2_256_digest:
            return ""
        blake2_256_re = re.compile(r"^[A-F0-9]{64}$", re.IGNORECASE)
        assert blake2_256_re.match(
            blake2_256_digest
        ), "blake2_256_digest is not a valid hex-encoded string."
        return blake2_256_digest

class ReleaseUpload(BaseModel):
    comment_text: Optional[str]
    # name: str
    # classifiers: Optional[Union[List[str], str]]
    keywords: Optional[str]
    filename : str
    has_sig: bool = False
    url: str = ""
    # license: Optional[str]

    version: str
    requires_python: Optional[str]
    platform: Optional[str]

    author: str
    author_email: Optional[EmailEmptyAllowedStr]

    maintainer: Optional[str]
    maintainer_email: Optional[EmailEmptyAllowedStr]

    size: Optional[int]
    # summary: Optional[str]
    # description: Optional[str]
    # description_content_type: Optional[str]

    # home_page: Optional[str]
    # package_url: Optional[str]
    # project_url: Optional[str]
    # bugtrack_url: Optional[str]
    # docs_url: Optional[str]
    # download_url: Optional[str]


    ##
    packagetype: str = Schema(None, alias="filetype")

    # pyversion: Optional[str]
    python_version: str = Schema(None, alias="pyversion")


    # comment: Optional[str]
    md5_digest: Optional[str]
    sha256_digest: Optional[str]
    blake2_256_digest: Optional[str]

    # @validator("name")
    # def validate_name(cls, name: str):
    #     name_re = re.compile(
    #         r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", re.IGNORECASE
    #     )
    #     assert name_re.match(
    #         name
    #     ), "Name should contains only letter, numeric, '.', '_', '-'"
    #     return normalize_package_name(name)

    @validator("version")
    def validate_version(cls, version: str):
        version_re = re.compile(r"^(?!\s).*(?<!\s)$")
        assert version_re.match(
            version
        ), "Version Can't have leading or trailing whitespace."
        return version


    # @validator("description_content_type")
    # def validate_description_content_type(cls, description_content_type: str):
    #     if not description_content_type:
    #         return ""
    #     allowed_content_type = {"text/plain", "text/x-rst", "text/markdown"}
    #     assert (
    #         description_content_type in allowed_content_type
    #     ), "Invalid description_content_type"
    #     return description_content_type

    @validator("requires_python")
    def validate_requires_python(cls, requires_python: str):
        if not requires_python:
            return ""
        assert is_valid_pep440_specifier(
            requires_python
        ), "requires_python is not a valid pep 440 specifier"
        return requires_python

    @validator("sha256_digest")
    def validate_md5_digest(cls, sha256_digest: str):
        if not sha256_digest:
            return ""
        sha256_re = re.compile(r"^[A-F0-9]{64}$", re.IGNORECASE)
        assert sha256_re.match(
            sha256_digest
        ), "sha256_digest is not a valid hex-encoded string."
        return sha256_digest

    @validator("blake2_256_digest")
    def validate_blake2_256_digestt(cls, blake2_256_digest: str):
        if not blake2_256_digest:
            return ""
        blake2_256_re = re.compile(r"^[A-F0-9]{64}$", re.IGNORECASE)
        assert blake2_256_re.match(
            blake2_256_digest
        ), "blake2_256_digest is not a valid hex-encoded string."
        return blake2_256_digest

    @root_validator
    def validate_all(cls, values):
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




