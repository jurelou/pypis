import httpx
from loguru import logger
from starlette import status
from dynaconf import settings
from pypis.services.http import HTTPClient

    
class PyPiProxy(HTTPClient):
    @staticmethod
    def _get_http_client() -> httpx.AsyncClient:
        return HTTPClient().client


    @classmethod
    def configure(cls, base_url : str = "https://pypi.org"):
        cls.base_url = base_url
        print("!!!!!", cls.client)
        pass


    @classmethod
    async def get_package_info(cls, package_name : str):
        endpoint = f"{cls.base_url}/pypi/{package_name}/json"
        async with cls._get_http_client() as client:
            r = await client.get(endpoint)
            if not r.status_code == status.HTTP_200_OK:
                return None
            return r.json()


    @classmethod
    async def get_package_version_info(cls, package_name : str, version : str):
        endpoint = f"{cls.base_url}/pypi/{package_name}/{version}/json"
        async with cls._get_http_client() as client:
            r = await client.get(endpoint)
            if not r.status_code == status.HTTP_200_OK:
                return None
            return r.json()
