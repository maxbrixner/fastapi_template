# ---------------------------------------------------------------------------- #

import fastapi
import logging

# ---------------------------------------------------------------------------- #

from contextlib import asynccontextmanager
from typing import AsyncGenerator

# ---------------------------------------------------------------------------- #

from app.database import database

# ---------------------------------------------------------------------------- #

logger = logging.getLogger("app.core")

# ---------------------------------------------------------------------------- #


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> AsyncGenerator:
    """
    Context manager for FastAPI lifespan events. Handles application startup
    and shutdown logic.
    """
    database.connect()

    logger.info("Application startup complete.")

    yield

    database.disconnect()

    logger.info("Application shutdown complete.")

# ---------------------------------------------------------------------------- #
