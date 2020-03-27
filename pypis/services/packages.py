import re
from typing import Optional

from asyncpg import Record
from dynaconf import settings

from packaging.specifiers import InvalidSpecifier, SpecifierSet


def is_valid_pep440_specifier(specifier):
    """Validate against PEP 440.

    https://www.python.org/dev/peps/pep-0440/
    """
    try:
        SpecifierSet(specifier)
        return True
    except InvalidSpecifier:
        return False


def normalize_package_name(name):
    """Normalise a package name as per PEP 426.

    https://www.python.org/dev/peps/pep-0426/
    """
    return re.sub(r"[-_.]+", "-", name).lower()
