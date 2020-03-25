from typing import Optional, List

from pypis.db.repositories.base import BaseRepository
from pypis.api.models.packages import PackageCreate
from pypis.db.models.packages import Package, Classifier
from pypis.db.models.releases import Release



        
class PackagesRepository(BaseRepository):
    def get_packages(self):
        return self.connection.query(Package).all()

    def get_package(self, package_name: str):
        return self.connection.query(Package).filter(Package.name == package_name).first()

    def _get_or_create_classifier(self, classifier_title: str):
        classifier_in_db = self.connection.query(Classifier).filter(Classifier.title == classifier_title).first()
        if classifier_in_db:
            return classifier_in_db
        new_classifier = Classifier(title=classifier_title)
        self.connection.add(new_classifier)
        return new_classifier

    def store_package(self, item: PackageCreate, releases: List[Release] = []):
        item_dict = item.dict()
        classifiers = item_dict.pop("classifiers", [])
        package = Package(**item_dict)

        classifiers = [self._get_or_create_classifier(c) for c in classifiers]
        package.classifiers.extend(classifiers)
        
        package.releases.extend(releases)
        self.connection.add(package)
        self.connection.commit()
        self.connection.refresh(package)
        return package