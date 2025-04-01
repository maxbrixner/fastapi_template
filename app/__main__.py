# ---------------------------------------------------------------------------- #

import fastapi
import fastapi.middleware.cors
import uvicorn
import logging
from contextlib import asynccontextmanager

# ---------------------------------------------------------------------------- #

from app.core.config import settings
from app.api.v1 import router as routerv1

# ---------------------------------------------------------------------------- #


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    """
    Context manager for FastAPI lifespan events. Handles application startup"
    and shutdown logic."
    """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("app")
    logger.info(f"INFO:     Starting up {settings.project_name}...")
    # todo: await init_db()
    logger.info("INFO:     Application startup complete.")
    yield
    logger.info("INFO:     Shutting down application...")
    # todo: await close_db_connections()
    logger.info("INFO:     Application shutdown complete.")

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
        fastapi.middleware.cors.CORSMiddleware,
        allow_origins=[str(origin).strip("/")
                       for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        fastapi.middleware.cors.CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ---------------------------------------------------------------------------- #


app.include_router(routerv1, prefix=settings.api_v1_str, tags=["v1"])

# ---------------------------------------------------------------------------- #


# --- Optional: Custom Exception Handlers ---
# You can add custom handlers here if needed, for example:
# from fastapi import Request, status
# from fastapi.responses import JSONResponse
# from app.core.exceptions import CustomAPIException
#
# @app.exception_handler(CustomAPIException)
# async def custom_api_exception_handler(request: Request, exc: CustomAPIException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail},
#     )

# ---------------------------------------------------------------------------- #


if __name__ == "__main__":
    uvicorn.run(app="app.__main__:app", host=settings.backend_host,
                port=settings.backend_port, reload=True)

# ---------------------------------------------------------------------------- #
