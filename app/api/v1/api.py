# ---------------------------------------------------------------------------- #

import fastapi

# ---------------------------------------------------------------------------- #

from app.api.v1.endpoints import user_router
from app.api.v1.endpoints import utils_router

# ---------------------------------------------------------------------------- #


router = fastapi.APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(user_router)
router.include_router(utils_router)


# ---------------------------------------------------------------------------- #
