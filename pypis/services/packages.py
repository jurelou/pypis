from pypis.services.proxy.pypi_proxy import PyPiProxy
import functools

from pydantic import BaseModel, Field
from typing import List, Optional
from dynaconf import settings
from pypis.api.models.packages import PackageCreate
from pypis.api.models.releases import ReleaseCreate
from pypis.services.utils import sort_list_by_version

async def download_and_replace_release_file(releases_repo):
    pass

async def fetch_package(package_name: str, packages_repo, releases_repo):
    package_data = await PyPiProxy.get_package_info(package_name)
    package_releases = package_data["releases"]
    package_info = package_data["info"]
    sorted_package_releases = sort_list_by_version(package_releases.keys())

    list_of_releases = []
    for version in sorted_package_releases[-settings.PACKAGES.MAX_PACKAGES_VERSION_CACHE:]:
        for release_data in package_releases[version]:
            release = await releases_repo.store_release(ReleaseCreate(version=version, sha256_digest=release_data["digests"]["sha256"], **release_data), package_name=package_name)
            list_of_releases.append(release)
    

    package = PackageCreate(**package_info)
    package_info = packages_repo.store_package(package, releases=list_of_releases)