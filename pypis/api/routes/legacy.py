from dynaconf import settings
from fastapi import APIRouter, Response, Depends
from loguru import logger

from pypis.services import html

from pypis.db.repositories.packages import PackagesRepository

from pypis.db.repositories.releases import ReleasesRepository
from pypis.api.dependencies.database import get_repository

from pypis.services import packages

router = APIRouter()


@router.get("/")
async def read_all_packages(
    packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)),
):
    # logger.info("!!!!! GETAMM")
    package_info = await PyPiProxy.get_package_info("ll")
    print("!!!!!", package_info)
    return packages_repo.get_packages()


@router.get("/{package_name}/")
async def read_package(package_name: str, packages_repo: PackagesRepository = Depends(get_repository(PackagesRepository)), releases_repo: ReleasesRepository = Depends(get_repository(ReleasesRepository))):
    package = packages_repo.get_package(package_name)
    if package:
        print("PAckage {} already present".format(package_name))
    else:
        await packages.fetch_package(package_name, packages_repo, releases_repo)




# @router.get("/{project_name}/")
# def read_packages(project_name: str):

#     tmp_requests = {
#         "requests-2.5.3.tar.gz": {
#             "href": "https://files.pythonhosted.org/packages/a6/36/06a7d4261f91552f21f017fe162d69df95ca7925d1436c8acf73283ee3d0/requests-2.5.3.tar.gz#sha256=55d7f5619daae94ec49ee81ed8ce5a2a47f0bbf8e06cf9466bee103eaf65"
#         },
#         "requests-2.6.0-py2.py3-none-any.whl": {
#             "href": "https://files.pythonhosted.org/packages/73/63/b0729be549494a3e31316437053bc4e0a8bb71a07a6ee6059434b8f1cd5f/requests-2.6.0-py2.py3-none-any.whl#sha256=fdb9af60d47ca80df0a213336019a34ff692d8fff361c349f2c8398fe460",
#         },
#         "requests-2.6.0.tar.gz": {
#             "href": "https://files.pythonhosted.org/packages/eb/70/237e11db04807a9409ed39997097118208e7814309d9bc3da7bb98d1fe3d/requests-2.6.0.tar.gz#sha256=1cdbed1f0e236f35efe919982a338e4fea378630933d3a787a04b74d75",
#         },
#     }

#     body = html.dicts_to_anchors(tmp_requests)
#     response = html.build_html_text(title="hey", body=body)

#     return Response(content=response, media_type="text/html")
