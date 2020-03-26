from asyncpg import Record
from dynaconf import settings

from pypis.api.models.packages import PackageCreate
from pypis.api.models.releases import ReleaseCreate
from pypis.db.repositories.packages import PackagesRepository
from pypis.db.repositories.releases import ReleasesRepository
from pypis.services.proxy.pypi_proxy import PyPiProxy
from pypis.services.utils import sort_list_by_version


async def fetch_package(
    package_name: str,
    packages_repo: PackagesRepository,
    releases_repo: ReleasesRepository,
) -> Record:
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
    package_data = await PyPiProxy.get_package_info(package_name)
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
                    **release_data
                ),
                package_name=package_name,
            )
            list_of_releases.append(release)

    package = PackageCreate(**package_info)
    return packages_repo.store_package(package, releases=list_of_releases)
