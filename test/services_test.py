# ---------------------------------------------------------------------------- #

import unittest
import os
from fastapi.templating import Jinja2Templates
from unittest.mock import patch, mock_open
from contextlib import ExitStack
from typing import Generator

# ---------------------------------------------------------------------------- #

from test._testcase import TestCase
from app.services import get_configuration, ConfigSchema
from app.services import setup_logger
from app.services import get_templates

# ---------------------------------------------------------------------------- #


class ConfigTest(TestCase):
    """
    Test cases for service operations.
    """

    def test_get_configuration(self) -> None:
        """
        Test case for loading the configuration.
        """
        get_configuration.cache_clear()
        with ExitStack() as stack:
            mock_env = stack.enter_context(
                patch.dict(os.environ, {"CONFIG": "test.json"})
            )
            mock_file = stack.enter_context(
                patch("pathlib.Path.open", unittest.mock.mock_open(
                    read_data='{}'))
            )

            config = get_configuration()
            assert config.backend.host == "0.0.0.0"
            mock_file.assert_called_once()
            assert isinstance(config, ConfigSchema)

# ---------------------------------------------------------------------------- #


class LoggingTest(TestCase):
    """
    Test cases for logging operations.
    """

    def test_setup_logger(self) -> None:
        """
        Test case for loading the logger configuration.
        """
        with ExitStack() as stack:
            mock_env = stack.enter_context(
                patch.dict(os.environ, {"LOGGING": "test.json"})
            )
            mock_file = stack.enter_context(
                patch("pathlib.Path.open", unittest.mock.mock_open(
                    read_data='{"version": 1}'))
            )
            mock_logger = stack.enter_context(
                patch("logging.config.dictConfig")
            )

            setup_logger()
            mock_file.assert_called_once()
            mock_logger.assert_called_once()

# ---------------------------------------------------------------------------- #


class TemplatesTest(TestCase):
    """
    Test cases for template operations via Jinja2.
    """

    def test_get_templates(self) -> None:
        """
        Test case for loading the Jinja2 templates.
        """
        get_configuration.cache_clear()
        get_templates.cache_clear()
        with ExitStack() as stack:
            mock_config = stack.enter_context(
                patch('app.services.templates.get_configuration',
                      return_value=ConfigSchema())
            )

            templates = get_templates()
            assert isinstance(templates, Jinja2Templates)

# ---------------------------------------------------------------------------- #
