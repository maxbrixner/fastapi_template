# ---------------------------------------------------------------------------- #

import fastapi

# ---------------------------------------------------------------------------- #

from app.schemas.utils import HealthSchema

# ---------------------------------------------------------------------------- #


router = fastapi.APIRouter(prefix="/utils", tags=["utils"])

# ---------------------------------------------------------------------------- #


@router.get("/health")
async def utils_health() -> HealthSchema:
    """
    Return the health of the api.
    """
    return HealthSchema(
        health="healthy",
        message="API is healthy",
    )

# ---------------------------------------------------------------------------- #
