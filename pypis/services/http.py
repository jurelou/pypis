import httpx
from dynaconf import settings

from pypis.services.filesystem import create_file_and_parents
from pypis.services.patterns import Singleton


class HTTPClient(Singleton):  # type: ignore
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=settings.PYPI_PROXY.TIMEOUT)

    @property
    def client(self) -> httpx.AsyncClient:
        """Return an httpx client instance."""
        return self._client


async def download_file(filename: str, file_url: str) -> str:
    """Download a file using httpx client.

    Args:
        filename (str): output filename where the file will be downloaded.
        file_url (str): Public url which will be used to retrieve the file.
    Returns:
        The downloaded file path.
    """
    client = HTTPClient().client
    print("URL {} to {}".format(file_url, filename))
    create_file_and_parents(filename)
    async with client.stream("GET", file_url) as response:
        with open(filename, "wb") as f:
            async for chunk in response.aiter_raw():
                f.write(chunk)
    return filename
