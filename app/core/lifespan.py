# ---------------------------------------------------------------------------- #

import fastapi
import logging

# ---------------------------------------------------------------------------- #

from contextlib import asynccontextmanager
from typing import AsyncGenerator

# ---------------------------------------------------------------------------- #

import app.database as database
import app.services as services

# ---------------------------------------------------------------------------- #

logger = logging.getLogger("app.core")

# ---------------------------------------------------------------------------- #


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> AsyncGenerator:
    """
    Context manager for FastAPI lifespan events. Handles application startup
    and shutdown logic.
    """
    config = services.get_configuration()

    database_instance = database.get_database()

    database_instance.connect()

    if config.workers.enabled:
        worker_pool = services.get_worker_pool()

    logger.info("Application startup complete.")

    yield

    database_instance.disconnect()

    if config.workers.enabled:
        worker_pool.shutdown(wait=True)

    logger.info("Application shutdown complete.")

# ---------------------------------------------------------------------------- #
