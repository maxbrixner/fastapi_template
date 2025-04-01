# ---------------------------------------------------------------------------- #

import pydantic
from typing import List

# ---------------------------------------------------------------------------- #


def load_settings():
    class Settings(pydantic.BaseModel):
        project_name: str = "project"
        project_description: str = "A FastAPI project template."
        project_version: str = "0.1.0"
        project_author: str = "Max Brixner"

        backend_host: str = "0.0.0.0"
        backend_port: int = 8000

        backend_enable_cors: bool = True
        backend_cors_origins: List[str] = []

        api_v1_str: str = "/api/v1"

    return Settings()

# ---------------------------------------------------------------------------- #


settings = load_settings()

# ---------------------------------------------------------------------------- #
