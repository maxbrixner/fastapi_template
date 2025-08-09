
# ---------------------------------------------------------------------------- #

import pydantic
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------- #


class DatabaseConfigSchema(pydantic.BaseModel):
    echo: bool = False
    max_overflow: int = 10
    pool_size: int = 5
    url: str

# ---------------------------------------------------------------------------- #


class AppConfigSchema(pydantic.BaseModel):
    author: str
    description: str
    summary: Optional[str] = None
    terms_of_service: Optional[str] = None
    title: str
    swagger_path: str = "/docs"


# ---------------------------------------------------------------------------- #


class BackendConfigSchema(pydantic.BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    root_path: str = ""
    max_workers: int = 4


# ---------------------------------------------------------------------------- #


class CorsConfigSchema(pydantic.BaseModel):
    allow_credentials: bool = False
    allow_headers: List[str] = []
    allow_methods: List[str] = []
    allow_origins: List[str] = []
    enabled: bool = True
    expose_headers: List[str] = []
    max_age: int = 600


# ---------------------------------------------------------------------------- #

class StaticFilesConfigSchema(pydantic.BaseModel):
    directory: str = "static"
    enabled: bool = False
    headers: Dict[str, str] = {}
    name: str = "static"
    path: str = "/static"

# ---------------------------------------------------------------------------- #


class TemplatesConfigSchema(pydantic.BaseModel):
    directory: str = "templates"
    enabled: bool = False
    headers: Dict[str, str] = {}

# ---------------------------------------------------------------------------- #


class GzipConfigSchema(pydantic.BaseModel):
    compression_level: int = 5
    enabled: bool = False
    minimum_size: int = 1000


# ---------------------------------------------------------------------------- #

class ConfigSchema(pydantic.BaseModel):
    backend: BackendConfigSchema = BackendConfigSchema()
    cors: CorsConfigSchema = CorsConfigSchema()
    database: DatabaseConfigSchema
    gzip: GzipConfigSchema = GzipConfigSchema()
    app: AppConfigSchema
    static_files: StaticFilesConfigSchema = StaticFilesConfigSchema()
    templates: TemplatesConfigSchema = TemplatesConfigSchema()

# ---------------------------------------------------------------------------- #
