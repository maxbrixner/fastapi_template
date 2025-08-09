# ---------------------------------------------------------------------------- #

import fastapi

# ---------------------------------------------------------------------------- #

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarlettHTTPException

# ---------------------------------------------------------------------------- #

import app.services as services
import app.core.exceptions as exceptions
import app.core.lifespan as lifespan
from app.api.v1 import router as router_api_v1
from app.gui.v1 import router as router_gui_v1

# ---------------------------------------------------------------------------- #


def get_version() -> str:
    try:
        import importlib.metadata
        version = importlib.metadata.version("app")
        return version
    except ImportError:
        return "unknown"

# ---------------------------------------------------------------------------- #


def create_app() -> fastapi.FastAPI:
    """
    Create and configure the FastAPI application instance.
    This function sets up the application with middleware, routers, and
    exception handlers. It also initializes the database connection and
    logging configuration.
    """
    services.setup_logger()

    config = services.get_configuration()

    app = fastapi.FastAPI(
        title=config.app.title,
        summary=config.app.summary,
        description=config.app.description,
        version=get_version(),
        terms_of_service=config.app.terms_of_service,
        root_path=config.backend.root_path,
        openapi_url=f"/openapi.json",
        docs_url=config.app.swagger_path,
        redoc_url=None,
        lifespan=lifespan.lifespan
    )

    if config.cors.enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors.allow_origins,
            allow_credentials=config.cors.allow_credentials,
            allow_methods=config.cors.allow_methods,
            allow_headers=config.cors.allow_headers,
            expose_headers=config.cors.expose_headers,
            max_age=config.cors.max_age
        )

    if config.static_files.enabled:
        from app.services.static import StaticFilesWithHeaders
        app.mount(
            config.static_files.path,
            StaticFilesWithHeaders(
                directory=config.static_files.directory),
            name=config.static_files.name
        )

    if config.templates.enabled:
        from app.services import TemplateHeaderMiddleware
        app.add_middleware(TemplateHeaderMiddleware)

    if config.gzip.enabled:
        app.add_middleware(
            GZipMiddleware,
            minimum_size=config.gzip.minimum_size,
            compresslevel=config.gzip.compression_level
        )

    app.include_router(router_api_v1)
    app.include_router(router_gui_v1)

    app.add_exception_handler(
        Exception, exceptions.exception_handler)
    app.add_exception_handler(
        NotImplementedError, exceptions.exception_handler)
    app.add_exception_handler(
        HTTPException, exceptions.http_exception_handler)
    app.add_exception_handler(
        StarlettHTTPException, exceptions.http_exception_handler)

    return app

# ---------------------------------------------------------------------------- #
