from fastapi import APIRouter, Depends, Response
from loguru import logger

from pypis.api.dependencies.database import get_repository
from pypis.db.repositories.packages import PackagesRepository
from pypis.db.repositories.releases import ReleasesRepository
from pypis.services import html, packages

router = APIRouter()


@router.get("/")
async def read_all_packages(
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
) -> None:
    """Get all the packages that have been registered.

    https://warehouse.readthedocs.io/api-reference/legacy/#get--simple-
    """


@router.get("/{package_name}/")
async def read_package(
    package_name: str,
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
    releases_repo: ReleasesRepository = Depends(get_repository(ReleasesRepository)),
) -> Response:
    """Get all of the distribution download URLs for the package name.

    https://warehouse.readthedocs.io/api-reference/legacy/#get--simple--project--
    """
    logger.info("Read package {}.".format(package_name))
    package = packages_repo.get_package(package_name)
    if not package:
        logger.info("Package {} not found. Retrieving from pypi.".format(package_name))
        package = await packages.fetch_package(
            package_name, packages_repo, releases_repo
        )

    anchors_list = releases_repo.package_releases_to_anchors_list(package.id)
    raw_html = html.build_html_text(body=anchors_list)
    return Response(content=raw_html, media_type="text/html")
