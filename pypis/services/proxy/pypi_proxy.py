from typing import Any

import httpx
from loguru import logger
from starlette import status

from pypis.services.http import HTTPClient


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
