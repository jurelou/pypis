from dynaconf import settings
import httpx
from pypis.services.patterns import Singleton
from pypis.services.filesystem import create_file_and_parents

class HTTPClient(Singleton):
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.PYPI_PROXY.TIMEOUT)

    @property
    def client(self):
        return self._client


async def download_file(filename: str, file_url: str):
    client = HTTPClient().client
    print("URL {} to {}".format(file_url, filename))
    create_file_and_parents(filename)
    async with client.stream('GET', file_url) as response:
        with open(filename, "wb") as f:
            async for chunk in response.aiter_raw():
                f.write(chunk)
    return filename