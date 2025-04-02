# ---------------------------------------------------------------------------- #

import logging
import os
import json
import pathlib

# ---------------------------------------------------------------------------- #


def setup_logging() -> None:
    filename = os.getenv("LOGGING", None)

    if not filename:
        raise Exception("LOGGING environment variable not set.")

    logging_file = pathlib.Path(__file__).parent.parent / \
        pathlib.Path("config") / \
        pathlib.Path(filename)

    with logging_file.open("r") as file:
        content = json.load(file)
        logging.config.dictConfig(content)

# ---------------------------------------------------------------------------- #
