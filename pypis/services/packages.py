import os
import re
from itertools import chain
from typing import List, Iterator

import stdlib_list
from dynaconf import settings
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.utils import canonicalize_name, canonicalize_version

from pypis.services.filesystem import create_file_and_parents


def canonicalize_package_version(version: str) -> str:
    """Return the normalized form of the version."""
    return str(canonicalize_version(version))


def is_standard_package(package_name: str) -> bool:
    """Check for collisions with Python Standard Library modules."""

    def _namespace_stdlib_list(module_list: List[str]) -> Iterator[str]:
        for module_name in module_list:
            parts = module_name.split(".")
            for i, part in enumerate(parts):
                yield ".".join(parts[: i + 1])

    stdlib_prohibited = {
        canonicalize_name(s.rstrip("-_.").lstrip("-_."))
        for s in chain.from_iterable(
            _namespace_stdlib_list(stdlib_list.stdlib_list(version))
            for version in stdlib_list.short_versions
        )
    }
    return canonicalize_name(package_name) in stdlib_prohibited


def create_package_filepath(
    package_name: str, version: str, filename: str, create: bool = True
) -> str:
    """Create a filepath for the project release."""
    file_path = os.path.join(package_name, version, filename)
    absolute_path = os.path.join(settings.PACKAGES.BASE_DIRECTORY, file_path)

    if create:
        create_file_and_parents(absolute_path)
    return absolute_path


def create_package_uri(package_name: str, version: str, filename: str) -> str:
    """Create an HTTP uri for the project release."""
    file_path = os.path.join(package_name, version, filename)
    return "{}/{}".format(settings.PACKAGES.HOSTED_FILES_URI, file_path)


def is_valid_pep440_specifier(specifier: str) -> bool:
    """Validate against PEP 440.

    https://www.python.org/dev/peps/pep-0440/
    """
    try:
        SpecifierSet(specifier)
        return True
    except InvalidSpecifier:
        return False


def normalize_package_name(name: str) -> str:
    """Normalise a package name as per PEP 426.

    https://www.python.org/dev/peps/pep-0426/
    """
    return re.sub(r"[-_.]+", "-", name).lower()
