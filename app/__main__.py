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
    title=config.project.name,
    description=config.project.description,
    version=config.project.version,
    root_path=config.backend.root_path,
    openapi_url=f"/openapi.json",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

# ---------------------------------------------------------------------------- #


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.allow_origins,
    allow_credentials=config.cors.allow_credentials,
    allow_methods=config.cors.allow_methods,
    allow_headers=config.cors.allow_headers,
    expose_headers=config.cors.expose_headers,
    max_age=config.cors.max_age
)

# ---------------------------------------------------------------------------- #


app.include_router(routerv1)

# ---------------------------------------------------------------------------- #


@app.exception_handler(Exception)
async def exception_handler(
    request: fastapi.Request,
    exception: Exception
) -> fastapi.responses.JSONResponse:
    """
    Exception handler for all unhandled exceptions.
    """
    logger.warning(
        f"Exception handled: '{exception}' for url '{request.url}'.")
    return fastapi.responses.JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
        headers=None
    )


# ---------------------------------------------------------------------------- #


@app.exception_handler(HTTPException)
@app.exception_handler(StarlettHTTPException)
async def http_exception_handler(
    request: fastapi.Request,
    exception: Exception
) -> fastapi.responses.JSONResponse:
    """
    Exception handler for all unhandled http exceptions.
    """
    logger.warning(
        f"HTTP Exception handled: '{exception}' for url '{request.url}'.")
    return fastapi.responses.JSONResponse(
        status_code=exception.status_code if hasattr(
            exception, 'status_code') else 500,
        content={"detail": str(exception.detail) if hasattr(
            exception, 'detail') else "An error occurred"},
        headers=exception.headers if hasattr(
            exception, 'headers') else None
    )

# ---------------------------------------------------------------------------- #


if __name__ == "__main__":
    """
    Main entry point for the application. Loads the configuration and starts
    the application server.
    """
    host = config.backend.host
    port = int(config.backend.port)

    uvicorn.run(app="app.__main__:app", host=host,
                port=port, reload=True)

# ---------------------------------------------------------------------------- #
