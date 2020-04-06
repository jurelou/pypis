import os
import shutil
from typing import List, Union

from asyncpg import Record
from starlette.datastructures import UploadFile

from pypis.api.models import PackageCreate, PackageUpload, ReleasePrivateUpload
from pypis.db.models import Package, Release, Classifier
from pypis.db.repositories.base import BaseRepository
from pypis.services.packages import (create_package_filepath,
                                     create_package_uri,
                                     canonicalize_package_version,
                                     check_is_valid_release)
from pypis.services.exceptions import DuplicateReleaseException



class PackagesRepository(BaseRepository):
    def get_packages(self) -> Union[Record, List[Record]]:
        """Get all packages."""
        return self.connection.query(Package).all()

    def get_package(self, package_name: str) -> Record:
        """Get a package by name."""
        return (
            self.connection.query(Package).filter(Package.name == package_name).first()
        )

    def _get_or_create_classifier(self, classifier_title: str) -> Record:
        classifier_in_db = (
            self.connection.query(Classifier)
            .filter(Classifier.title == classifier_title)
            .first()
        )
        if classifier_in_db:
            return classifier_in_db
        new_classifier = Classifier(title=classifier_title)
        self.connection.add(new_classifier)
        return new_classifier

    def store_package(
        self, package: PackageCreate, releases: List[Release] = []
    ) -> Record:
        """Store a package in the database.

        releases can be provided as a argument, they will be added to the package.
        Args:
            package (Package): Instance of a `Package` ORM model.
            releases (Optional[List[Release]]): Optional list of `Release` ORM model.
        Returns:
            Return an ORM model of the freshly created package.
        """
        package_dict = package.dict()
        classifiers = package_dict.pop("classifiers", [])
        package_db = Package(**package_dict) 
        classifiers = [self._get_or_create_classifier(c) for c in classifiers]
        package_db.classifiers.extend(classifiers)
        if releases:
            package_db.releases.extend(releases)
        self.connection.add(package_db)
        self.connection.commit()
        self.connection.refresh(package_db)
        return package_db

    def _add_release_to_package(self, package_name: str, release: Release) -> Record:
        package = self.get_package(package_name)
        version = canonicalize_package_version(release.version)
        if not package:
            return None
        package.releases.append(release)
        self.connection.commit()
        return package


    async def store_private_package(
        self,
        package_file: UploadFile,
        package_model: PackageUpload,
        release: ReleasePrivateUpload,
    ) -> Record:
        """Store a private release."""
        package_name = package_model.name
        package = self.get_package(package_name)
        if not package:
            package = self.store_package(package_model)

        q = self.connection.query(Release).filter(
                (Release.package_id == package.id)
                & (Release.version == release.version)
                & (Release.packagetype == release.packagetype)).first()
        if q:
            raise DuplicateReleaseException(f"A release for {package.name} version {release.version} (build: {release.packagetype}) already exists")


        q = self.connection.query(Release).filter(Release.filename == release.filename).first()
        if q:
            raise DuplicateReleaseException(f"A release file for {package.name} already exists: {release.filename}")



        absolute_file_path = create_package_filepath(
            package_name, release.version, release.filename
        )
        with open(absolute_file_path, "wb+") as f:
            shutil.copyfileobj(package_file.file, f)

        release.url = create_package_uri(
            package_name, release.version, release.filename
        )
        release.size = os.stat(absolute_file_path).st_size

        release_db = Release(**release.dict())



        if check_is_valid_release(package, release_db, absolute_file_path):
            self._add_release_to_package(package_name, release_db)
