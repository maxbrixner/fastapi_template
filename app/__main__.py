# ---------------------------------------------------------------------------- #

import fastapi
import uvicorn
import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarlettHTTPException

from contextlib import asynccontextmanager

# ---------------------------------------------------------------------------- #

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import database
from app.api.v1 import router as routerv1

# ---------------------------------------------------------------------------- #


logger = logging.getLogger("app")

# ---------------------------------------------------------------------------- #


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    """
    Context manager for FastAPI lifespan events. Handles application startup"
    and shutdown logic."
    """
    setup_logging()

    logger.info("Starting up application...")
    database.connect()
    logger.info("Application startup complete.")

    yield

    logger.info("Shutting down application...")
    database.disconnect()
    logger.info("Application shutdown complete.")

# ---------------------------------------------------------------------------- #


settings.load_settings()

# ---------------------------------------------------------------------------- #


app = fastapi.FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.project_version,
    openapi_url=f"/openapi.json",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

# ---------------------------------------------------------------------------- #


if settings.backend_enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/")
                       for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
):
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
):
    logger.warning(f"HTTP Exception handled: {exception}")
    return fastapi.responses.JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

# ---------------------------------------------------------------------------- #


if __name__ == "__main__":
    uvicorn.run(app="app.__main__:app", host=settings.backend_host,
                port=settings.backend_port, reload=True)

# ---------------------------------------------------------------------------- #
