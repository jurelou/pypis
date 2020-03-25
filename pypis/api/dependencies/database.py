from typing import AsyncGenerator, Callable
from fastapi import Depends

from pypis.db.database import get_db
from pypis.db.repositories.base import BaseRepository


def get_repository(repo_type: BaseRepository) -> Callable:
    async def _get_repo(pool=Depends(get_db),) -> AsyncGenerator[BaseRepository, None]:
        yield repo_type(pool)

    return _get_repo
