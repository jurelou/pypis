from typing import List, Union

from asyncpg import Record

from pypis.api.models.packages import PackageCreate
from pypis.db.models.packages import Classifier, Package
from pypis.db.models.releases import Release
from pypis.db.repositories.base import BaseRepository


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
