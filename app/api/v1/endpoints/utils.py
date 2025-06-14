# ---------------------------------------------------------------------------- #

import fastapi

# ---------------------------------------------------------------------------- #

import app.schemas as schemas

# ---------------------------------------------------------------------------- #


router = fastapi.APIRouter(prefix="/utils", tags=["utils"])

# ---------------------------------------------------------------------------- #


@router.get("/health")
async def utils_health() -> schemas.HealthSchema:
    """
    Return the health of the api.
    """
    return schemas.HealthSchema(
        health=schemas.HealthEnum.HEALTHY,
        message="API is healthy",
    )

# ---------------------------------------------------------------------------- #
