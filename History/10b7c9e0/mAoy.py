"""Scaffolding template for Python packages."""

import logging

from atoolbox import (
    BaseFile,
    FileHandler,
    JsonFile,
    TextFile,
    UffFile,
)
from .dbfile import DbFile
from .SQLHandler import NVHBrake, SQLite3Code

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

logger.info("Package loaded")

__author__ = "Andreas Hofer"
__version__ = "0.0.1"
