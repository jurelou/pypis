import os
import shutil
from typing import List, Union
from starlette.datastructures import UploadFile
from asyncpg import Record

from pypis.api.models.packages import PackageCreate, PackageUpload
from pypis.api.models.releases import ReleasePrivateUpload
from pypis.db.models.classifiers import Classifier
from pypis.db.models.packages import Package
from pypis.db.models.releases import Release
from pypis.db.repositories.base import BaseRepository
from pypis.services.packages import (create_package_filepath,
                                     create_package_uri,
                                     is_standard_package)


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

        package_db.releases.extend(releases)
        self.connection.add(package_db)
        self.connection.commit()
        self.connection.refresh(package_db)
        return package_db

    async def store_private_package(
        self,
        package_file: UploadFile,
        package_model: PackageUpload,
        release: ReleasePrivateUpload
    ) -> Record:
        """Store a private release."""
        print("!!!!!!", type(package_file))
        package_name = package_model.name

        package = self.get_package(package_name)

        absolute_file_path = create_package_filepath(
            package_name, release.version, release.filename
        )
        with open(absolute_file_path, "wb+") as f:
            shutil.copyfileobj(package_file.file, f)

        release.url = create_package_uri(
            package_name, release.version, release.filename
        )
        release.size = os.stat(absolute_file_path).st_size

        if is_standard_package(package_name):
            print("STANDARD PACKAGE")
            return "Its a standard package ..."

        if package:
            print("PACKAGE {} already exists.".format(package_name))
        else:
            print("PACKAGE {} does not exists.".format(package_name))
            release_db = Release(**release.dict())
            self.store_package(package_model, releases=[release_db])
