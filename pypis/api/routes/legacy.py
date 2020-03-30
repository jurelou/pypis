from fastapi import APIRouter, Depends, Request, Response
from loguru import logger
from starlette import status
from starlette.responses import JSONResponse

from pypis.api.dependencies.database import get_repository
from pypis.api.models.packages import PackageUpload
from pypis.api.models.releases import ReleasePrivateUpload
from pypis.db.repositories.packages import PackagesRepository
from pypis.db.repositories.releases import ReleasesRepository
from pypis.services import html
from pypis.services.packages import normalize_package_name
from pypis.services.proxy.pypi_proxy import PyPiProxy

router = APIRouter()


@router.get("/")
async def read_all_packages(
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
) -> Response:
    """Get all the packages that have been registered.

    https://warehouse.readthedocs.io/api-reference/legacy/#get--simple-
    """
    packages = packages_repo.get_packages()
    packages_dict = {
        p.name: {"href": "/api/simple/{}/".format(p.name)} for p in packages
    }
    anchors = html.dicts_to_anchors(packages_dict)
    raw_html = html.build_html_text(body=anchors)
    return Response(content=raw_html, media_type="text/html")


@router.post("/")
async def create_package(
    request: Request,
    releases_repo: ReleasesRepository = Depends(get_repository(ReleasesRepository)),
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
) -> JSONResponse:
    """Upload packages.

    https://warehouse.readthedocs.io/api-reference/legacy/#get--simple-
    """
    form = await request.form()

    package_file = form["content"]
    if not package_file or not package_file.filename:
        return JSONResponse(
            status=status.HTTP_400_BAD_REQUEST, content="Empty package file."
            )

    package = PackageUpload(**form)
    release = ReleasePrivateUpload(**form, filename=package_file.filename)
    await packages_repo.store_private_package(package_file, package, release)


@router.get("/{package_name}/")
async def read_package(
    package_name: str,
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
    releases_repo: ReleasesRepository = Depends(get_repository(ReleasesRepository)),
) -> Response:
    """Get all of the distribution download URLs for the package name.

    https://warehouse.readthedocs.io/api-reference/legacy/#get--simple--project--
    """
    package_name = normalize_package_name(package_name)
    logger.info("Read package {}.".format(package_name))
    package = packages_repo.get_package(package_name)
    if not package:
        logger.info("Package {} not found. Retrieving from pypi.".format(package_name))
        package = await PyPiProxy.fetch_package(
            package_name, packages_repo, releases_repo
        )

    anchors_list = releases_repo.package_releases_as_anchors(package.id)
    raw_html = html.build_html_text(body=anchors_list)
    return Response(content=raw_html, media_type="text/html")
