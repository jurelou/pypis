from asyncpg.connection import Connection


class BaseRepository:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    @property
    def connection(self) -> Connection:
        """Return an sqlalchemy connection."""
        return self._conn
