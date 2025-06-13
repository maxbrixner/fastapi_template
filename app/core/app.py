

# ---------------------------------------------------------------------------- #

import fastapi

# ---------------------------------------------------------------------------- #

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarlettHTTPException

# ---------------------------------------------------------------------------- #

from app.api.v1 import router as routerv1
from app.services import get_configuration, setup_logger
from app.core.exceptions import *
from app.core.lifespan import *

# ---------------------------------------------------------------------------- #


def create_app() -> fastapi.FastAPI:
    """
    Create and configure the FastAPI application instance.
    This function sets up the application with middleware, routers, and
    exception handlers. It also initializes the database connection and
    logging configuration.
    """
    setup_logger()

    config = get_configuration()

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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors.allow_origins,
        allow_credentials=config.cors.allow_credentials,
        allow_methods=config.cors.allow_methods,
        allow_headers=config.cors.allow_headers,
        expose_headers=config.cors.expose_headers,
        max_age=config.cors.max_age
    )

    app.include_router(routerv1)

    app.add_exception_handler(Exception, exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarlettHTTPException, http_exception_handler)

    return app

# ---------------------------------------------------------------------------- #
