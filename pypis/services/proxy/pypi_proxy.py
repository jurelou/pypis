import re
from typing import Any, Optional

import httpx
from asyncpg import Record
from dynaconf import settings
from loguru import logger
from starlette import status

from pypis.api.models.packages import PackageCreate
from pypis.api.models.releases import ReleaseCreate
from pypis.db.repositories.packages import PackagesRepository
from pypis.db.repositories.releases import ReleasesRepository
from pypis.services.http import HTTPClient
from pypis.services.utils import sort_list_by_version


class PyPiProxy(HTTPClient):
    @staticmethod
    def _get_http_client() -> httpx.AsyncClient:
        """Get an instance of HTTPClient."""
        return HTTPClient().client

    @classmethod
    def configure(cls, base_url: str = "https://pypi.org") -> None:
        """Configure Pypi base url."""
        logger.info("Using pypi proxy: {}".format(base_url))
        cls.base_url = base_url

    @classmethod
    async def get_package_info(cls, package_name: str) -> Any:
        """Retrieve package info.

        Requests PyPi JSON API using /pypi/<package_name>/json endpoint
        https://warehouse.readthedocs.io/api-reference/json/#get--pypi--project_name--json
        Args:
            package_name (str): Name of the package from which
            we will retrieve informations.
        Returns:
            Json package data.
        """
        logger.info("Request pypi json API for package: {}".format(package_name))
        endpoint = f"{cls.base_url}/pypi/{package_name}/json"
        async with cls._get_http_client() as client:
            r = await client.get(endpoint)
            if not r.status_code == status.HTTP_200_OK:
                return None
            return r.json()

    @classmethod
    async def get_package_version_info(cls, package_name: str, version: str) -> Any:
        """Retrieve package version info.

        Requests PyPi JSON API using /pypi/<package_name>/<version>/json endpoint
        https://warehouse.readthedocs.io/api-reference/json/#get--pypi--project_name---version--json
        Args:
            package_name (str): Name of the package from which
            we will retrieve informations.
            version (str): Version of the package
        Returns:
            Json package data.
        """
        logger.info(
            "Request pypi json API for package: {} version {}".format(
                package_name, version
            )
        )
        endpoint = f"{cls.base_url}/pypi/{package_name}/{version}/json"
        async with cls._get_http_client() as client:
            r = await client.get(endpoint)
            if not r.status_code == status.HTTP_200_OK:
                return None
            return r.json()

    @classmethod
    async def fetch_package(
        cls,
        package_name: str,
        packages_repo: PackagesRepository,
        releases_repo: ReleasesRepository,
    ) -> Optional[Record]:
        """Fetch a package from PyPi and stores it.

        Releases from this package will be download and stored localy.
        To avoid downloading too many releases we limit the amout of releases by
        the configuration field: packages.MAX_PACKAGES_VERSION_CACHE.
        For example, if MAX_PACKAGES_VERSION_CACHE is 10,
        the 10 latests releases will be downloaded
        args:
            package_name (str): Package name from which will retrieve releases.
            packages_repo (PackagesRepository): fastapi PackagesRepository dependency
            releases_repo (ReleasesRepository): fastapi ReleasesRepository dependency
        returns:
            The ORM instance of the created package.
        """
        package_data = await cls.get_package_info(package_name)
        if not package_data:
            return None
        package_releases = package_data["releases"]
        package_info = package_data["info"]
        sorted_package_releases = sort_list_by_version(package_releases.keys())

        list_of_releases = []
        max_packages_history = -settings.PACKAGES.MAX_PACKAGES_VERSION_CACHE
        for version in sorted_package_releases[max_packages_history:]:
            for release_data in package_releases[version]:
                release = await releases_repo.store_release(
                    ReleaseCreate(
                        version=version,
                        sha256_digest=release_data["digests"]["sha256"],
                        **release_data,
                    ),
                    package_name=package_name,
                )
                list_of_releases.append(release)

        package = PackageCreate(**package_info)
        return packages_repo.store_package(package, releases=list_of_releases)
