import os
import re
import zipfile
import tarfile
from itertools import chain
from typing import Iterator, List

import stdlib_list
from dynaconf import settings
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.utils import canonicalize_name, canonicalize_version
from pypis.db.models import Package, Release

from pypis.services.filesystem import create_file_and_parents

from pypis.services.exceptions import InvalidReleaseException


_allowed_platforms = {
    "any",
    "win32",
    "win_amd64",
    "win_ia64",
    "manylinux1_x86_64",
    "manylinux1_i686",
    "manylinux2010_x86_64",
    "manylinux2010_i686",
    "manylinux2014_x86_64",
    "manylinux2014_i686",
    "manylinux2014_aarch64",
    "manylinux2014_armv7l",
    "manylinux2014_ppc64",
    "manylinux2014_ppc64le",
    "manylinux2014_s390x",
    "linux_armv6l",
    "linux_armv7l",
}

_macosx_platform_re = re.compile(r"macosx_10_(\d+)+_(?P<arch>.*)")
_macosx_arches = {
    "ppc",
    "ppc64",
    "i386",
    "x86_64",
    "intel",
    "fat",
    "fat32",
    "fat64",
    "universal",
}

def _valid_platform_tag(platform_tag):
    if platform_tag in _allowed_platforms:
        return True
    m = _macosx_platform_re.match(platform_tag)
    if m and m.group("arch") in _macosx_arches:
        return True
    return False

def _zipfile_contains_file(filepath: str, filename_to_check: str):
    try:
        with zipfile.ZipFile(filepath, "r") as zfp:
            for zipname in zfp.namelist():
                parts = os.path.split(zipname)
                if len(parts) == 2 and parts[1] == filename_to_check:
                    break  # pragma: no branch
            else:
                return False
    except zipfile.BadZipFile:
        return False
    return True

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


def check_is_valid_release(package: Package, release: Release, filepath: str) -> bool:
        if is_standard_package(package.name):
            raise InvalidReleaseException(f"{package.name} is a standard python package.")

        if zipfile.is_zipfile(filepath):
            print("{} is a zipfile".format(filepath))
            with zipfile.ZipFile(filepath) as zfp:
                for zinfo in zfp.infolist():
                    if zinfo.compress_type not in {
                        zipfile.ZIP_STORED,
                        zipfile.ZIP_DEFLATED,
                    }:
                        raise InvalidReleaseException("Invalid zip compression method. Should be ZIP_STORED or ZIP_DEFLATED")
        
        tar_filenames_re = re.compile(r"\.(?:tar$|t(?:ar\.)?(?P<z_type>gz|bz2)$)")
        safe_zipnames = re.compile(r"(purelib|platlib|headers|scripts|data).+", re.I)


        tar_fn_match = tar_filenames_re.search(filepath)
        if tar_fn_match:
            z_type = tar_fn_match.group("z_type") or ""
            try:
                with tarfile.open(filepath, f"r:{z_type}") as tar:
                    bad_tar = True
                    member = tar.next()
                    while member:
                        parts = os.path.split(member.name)
                        if len(parts) == 2 and parts[1] == "PKG-INFO":
                            bad_tar = False
                        member = tar.next()
                    if bad_tar:
                        raise InvalidReleaseException("Invalid tarfile.")
            except tarfile.ReadError:
                raise InvalidReleaseException("Could not read archive. Invalid tar file.")

        elif filepath.endswith(".exe"):
            if release.packagetype != "bdist_wininst":
                raise InvalidReleaseException("Package should be of type bdist_wininst.")
            try:
                with zipfile.ZipFile(filepath, "r") as zfp:
                    for zipname in zfp.namelist():
                        if not safe_zipnames.match(zipname):
                            raise InvalidReleaseException("Invalid zip filename.")
            except zipfile.BadZipFile:
                raise InvalidReleaseException("Could not read zipfile.")

        elif filepath.endswith(".msi"):
            if release.packagetype != "bdist_msi":
                raise InvalidReleaseException("Package should be of type bdist_msi.")

        elif filepath.endswith(".zip") or filepath.endswith(".egg"):
            if not _zipfile_contains_file(filepath, "PKG-INFO"):
                raise InvalidReleaseException("Package should contain PKG-INFO file.")

        elif filepath.endswith(".whl"):
            if not _zipfile_contains_file(filepath, "WHEEL"):
                raise InvalidReleaseException("Package should contain WHEEL file.")
            wheel_file_re = re.compile(
                r"""
                ^
                (?P<namever>(?P<name>.+?)(-(?P<ver>\d.+?))?)
                (
                    (-(?P<build>\d.*?))?
                    -(?P<pyver>.+?)
                    -(?P<abi>.+?)
                    -(?P<plat>.+?)
                    (?:\.whl|\.dist-info)
                )
                $
                """,
                re.VERBOSE,
            )
            wheel_info = wheel_file_re.match(filepath)
            plats = wheel_info.group("plat").split(".")
            for plat in plats:
                if not _valid_platform_tag(plat):
                    raise InvalidReleaseException("Invalid platform tag.")
        return True


def canonicalize_package_version(version: str) -> str:
    """Return the normalized form of the version."""
    return str(canonicalize_version(version))


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
