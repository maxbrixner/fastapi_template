# ---------------------------------------------------------------------------- #

import pydantic
import pathlib
import os
import json
from typing import Any, List

# ---------------------------------------------------------------------------- #


class Settings():
    """
    Load and access application settings.
    """
    class SettingsSchema(pydantic.BaseModel):
        project_name: str
        project_description: str
        project_version: str
        project_author: str

        backend_host: str
        backend_port: int

        backend_enable_cors: bool
        backend_cors_origins: List[str]

    _settings: SettingsSchema | None

    def __init__(self) -> None:
        self._settings = None

    def load_settings(self) -> None:
        """
        Load settings from a json file.
        """
        filename = os.getenv("SETTINGS", None)

        if not filename:
            raise Exception("SETTINGS environment variable not set.")

        settings_file = pathlib.Path(__file__).parent.parent / \
            pathlib.Path("config") / \
            pathlib.Path(filename)

        with settings_file.open("r") as file:
            content = json.load(file)
            self._settings = self.SettingsSchema(**content)

    def __getattr__(self, name: str) -> Any:
        """
        Get the attribute from the settings.
        """
        if name == "_settings":
            return self.__dict__["_settings"]

        settings = self.__dict__["_settings"]

        if not settings:
            raise Exception("Settings not loaded. Call load_settings() first.")

        if not hasattr(settings, name):
            raise AttributeError(f"Settings object has no attribute '{name}'")

        return getattr(settings, name)

# ---------------------------------------------------------------------------- #


settings = Settings()

# ---------------------------------------------------------------------------- #
