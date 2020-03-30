from typing import Optional
import os
from fastapi import (APIRouter,
                     Depends,
                     Request,
                     Response,
                     )
from loguru import logger
from starlette import status
import shutil
from pypis.api.dependencies.database import get_repository
from pypis.api.models.packages import PackageUpload, PackageCreate
from pypis.api.models.releases import ReleaseUpload
from pypis.db.models.releases import Release

from pypis.db.repositories.packages import PackagesRepository
from pypis.db.repositories.releases import ReleasesRepository
from pypis.services import html
from pypis.services.proxy.pypi_proxy import PyPiProxy
from pypis.services.packages import is_standard_package, create_package_filepath,create_package_uri, normalize_package_name

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
    releases_repo: ReleasesRepository = Depends(get_repository(ReleasesRepository)),
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
) -> None:
    """Upload packages.

    https://warehouse.readthedocs.io/api-reference/legacy/#get--simple-
    """
    form = await request.form()


    package_file = form["content"]
    if not package_file or not package_file.filename:
        print("NO FILE PKF PRIVIDED")
        return "NO PACKAGE FILE"
    
    package_model = PackageUpload(**form)
    release = ReleaseUpload(**form, filename=package_file.filename)
    package_name = package_model.name

    package = packages_repo.get_package(package_name)


    absolute_file_path = create_package_filepath(package_name, release.version, release.filename)
    with open(absolute_file_path, 'wb+') as f:
            shutil.copyfileobj(package_file.file, f)

    release.url = create_package_uri(package_name, release.version, release.filename)
    release.size = os.stat(absolute_file_path).st_size

    if is_standard_package(package_name):
        print("STANDARD PACKAGE")
        return "Its a standard package ..."


    if package:
        print("PACKAGE {} already exists.".format(package_name))
    else:
        print("PACKAGE {} does not exists.".format(package_name))
        release_db = Release(**release.dict())
        packages_repo.store_package(package_model, releases=[release_db])
    # print("!!!", dict(form_data))
    # print("!!", form_data["content"])
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
