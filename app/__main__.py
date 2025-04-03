# ---------------------------------------------------------------------------- #

import fastapi
import uvicorn
import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarlettHTTPException

from contextlib import asynccontextmanager

from typing import AsyncGenerator

# ---------------------------------------------------------------------------- #

from app.core import config
from app.database import database
from app.api.v1 import router as routerv1

# ---------------------------------------------------------------------------- #


logger = logging.getLogger("app")

config.setup_logging()

config.load_configuration()

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


app = fastapi.FastAPI(
    title=config.project_name,
    description=config.project_description,
    version=config.project_version,
    openapi_url=f"/openapi.json",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

# ---------------------------------------------------------------------------- #


if config.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_allow_origins,
        allow_credentials=config.cors_allow_credentials,
        allow_methods=config.cors_allow_methods,
        allow_headers=config.cors_allow_headers
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ---------------------------------------------------------------------------- #


app.include_router(routerv1)

# ---------------------------------------------------------------------------- #


@app.exception_handler(Exception)
async def exception_handler(
    request: fastapi.Request,
    exception: Exception
) -> fastapi.responses.JSONResponse:
    logger.warning(f"Exception handled: {exception}")
    return fastapi.responses.JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


# ---------------------------------------------------------------------------- #


@app.exception_handler(HTTPException)
@app.exception_handler(StarlettHTTPException)
async def http_exception_handler(
    request: fastapi.Request,
    exception: Exception
) -> fastapi.responses.JSONResponse:
    logger.warning(f"HTTP Exception handled: {exception}")
    return fastapi.responses.JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

# ---------------------------------------------------------------------------- #


if __name__ == "__main__":
    host = config.backend_host
    port = int(config.backend_port)

    uvicorn.run(app="app.__main__:app", host=host,
                port=port, reload=True)

# ---------------------------------------------------------------------------- #
