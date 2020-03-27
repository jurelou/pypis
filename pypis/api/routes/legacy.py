from typing import Optional

from fastapi import (APIRouter,
                     Depends,
                     File,
                     Form,
                     Request,
                     Response,
                     UploadFile)
from loguru import logger
from starlette import status

from pypis.api.dependencies.database import get_repository
from pypis.api.models.packages import PackageUpload
from pypis.db.repositories.packages import PackagesRepository
from pypis.db.repositories.releases import ReleasesRepository
from pypis.services import html, packages
from pypis.services.proxy.pypi_proxy import PyPiProxy

router = APIRouter()


@router.get("/")
async def read_all_packages(
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
) -> None:
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
    # protocol_version: str = Form(...),
    # md5_digest: str = Form(...),
    # filetype: str = Form(...),
    # pyversion: Optional[str] = Form(None),
    # metadata_version: str = Form(...),
    # name: str = Form(...),
    # version: str = Form(...),
    # content: UploadFile = File(...),
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
) -> None:
    """Get all the packages that have been registered.

    https://warehouse.readthedocs.io/api-reference/legacy/#get--simple-
    """
    form_data = await request.form()
    package_file = form_data["content"]
    PackageUpload(**form_data)
    # print("!!!", dict(form_data))
    # print("!!", form_data["content"])
    pass
    # print(protocol_version)
    # print(md5_digest)
    # print("!!!", pyversion)
    # print(metadata_version)
    # print(name)
    # print(version)
    # print(content.filename)
    # if protocol_version != "1":
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown protocol version."
    #     )


@router.get("/{package_name}/")
async def read_package(
    package_name: str,
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
    releases_repo: ReleasesRepository = Depends(get_repository(ReleasesRepository)),
) -> Response:
    """Get all of the distribution download URLs for the package name.

    https://warehouse.readthedocs.io/api-reference/legacy/#get--simple--project--
    """
    package_name = packages.normalize_package_name(package_name)
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
