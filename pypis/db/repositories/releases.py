import os
from typing import Optional, List
from dynaconf import settings
from pypis.db.repositories.base import BaseRepository

from pypis.api.models.releases import ReleaseCreate
from pypis.db.models.releases import Release
from pypis.services.http import download_file


        
class ReleasesRepository(BaseRepository):
    def get_releases(self):
        return self.connection.query(Release).all()


    async def store_release(self, item: ReleaseCreate, package_name: str):
        db_item = Release(**item.dict())

        # download_file()
        file_path = os.path.join(settings.PACKAGES.BASE_DIRECTORY, package_name, item.version,item.filename)
        await download_file(file_path, item.url)

        self.connection.add(db_item)
        self.connection.commit()
        self.connection.refresh(db_item)
        
        return db_item
