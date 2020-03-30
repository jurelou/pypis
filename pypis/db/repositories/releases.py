import os
from typing import List, Union

from asyncpg import Record
from dynaconf import settings

from pypis.api.models.releases import ReleaseFromPypi
from pypis.db.models.releases import Release
from pypis.db.repositories.base import BaseRepository
from pypis.services.html import dicts_to_anchors
from pypis.services.http import download_file


class ReleasesRepository(BaseRepository):
    def get_releases(self) -> Union[Record, List[Record]]:
        """Get all releases."""
        return self.connection.query(Release).all()

    def get_package_releases(self, package_id: int) -> Union[Record, List[Record]]:
        """Get all releases for a given package id."""
        return (
            self.connection.query(Release)
            .filter(Release.package_id == package_id)
            .all()
        )

    async def store_release(
        self, release: ReleaseFromPypi, package_name: str
    ) -> Record:
        """Download and store a release.

        Example:
            The release file `foo.gz` version `0.0.1` from the package `bar`
            will be stored in `/bar/0.0.1/foo.gz`
            If the release contains a signature,
            it will be stored in `/bar/0.0.1/foo.gz.asc`
        Args:
            release (ReleaseCreate): ReleaseCreate pydantic model.
            package_name: (str): Package name which this release belongs to.
        Returns:
            The newly created release ORM model.
        """
        db_item = Release(**release.dict())

        file_path = os.path.join(package_name, release.version, release.filename)
        absolute_file_path = os.path.join(settings.PACKAGES.BASE_DIRECTORY, file_path)
        if release.has_sig:
            absolute_sig_path = "".join([absolute_file_path, ".asc"])
            await download_file(absolute_sig_path, "".join([release.url, ".asc"]))
        await download_file(absolute_file_path, release.url)

        db_item.url = "{}/{}".format(settings.PACKAGES.HOSTED_FILES_URI, file_path)
        self.connection.add(db_item)
        self.connection.commit()
        self.connection.refresh(db_item)

        return db_item

    def package_releases_as_anchors(self, package_id: int) -> str:
        """Retrieve all releases from a package as an HTML list of anchors."""
        releases = self.get_package_releases(package_id)
        release_dict = {}
        for release in releases:
            checksum = ""
            if release.sha256_digest:
                checksum = "#sha256={}".format(release.sha256_digest)
            elif release.md5_digest:
                checksum = "#md5={}".format(release.md5_digest)
            release_dict[release.filename] = {"href": "".join([release.url, checksum])}
            if hasattr(release, "has_sig"):
                release_dict[release.filename]["data-gpg-sig"] = release.has_sig
            if hasattr(release, "requires_python") and release.requires_python:
                release_dict[release.filename][
                    "data-requires-python"
                ] = release.requires_python

        return dicts_to_anchors(release_dict)
