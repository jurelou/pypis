import asyncpg
from fastapi import FastAPI
from loguru import logger

from dynaconf import settings


async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to {0}", repr(settings.DATABASE.URL))

    app.state.pool = await asyncpg.create_pool(
        str(settings.DATABASE.URL),
        min_size=settings.DATABASE.MIN_CONNECTIONS_COUNT,
        max_size=settings.DATABASE.MAX_CONNECTIONS_COUNT,
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")