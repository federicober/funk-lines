"""Common setup for all tests."""
import logging
import os

if os.getenv("FUNK_LINES_DEBUG"):
    logger: logging.Logger = logging.getLogger("funk_lines")
    logger.setLevel(logging.DEBUG)
    handler: logging.StreamHandler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s"))
    logger.addHandler(handler)
