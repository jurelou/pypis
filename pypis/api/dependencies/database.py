from typing import AsyncGenerator, Callable, Type

from fastapi import Depends
from sqlalchemy.orm import Session

from pypis.db.database import get_db
from pypis.db.repositories.base import BaseRepository


def get_repository(repo_type: Type[BaseRepository]) -> Callable:
    """Return a repository Callable for a given repository type.

    Args:
        repo_type (type): Repository type (should inherit from BaseRepository)
    Returns:
        A callable repository from the given type.
    """

    async def _get_repo(
        session: Session = Depends(get_db),
    ) -> AsyncGenerator[BaseRepository, None]:
        yield repo_type(session)

    return _get_repo
