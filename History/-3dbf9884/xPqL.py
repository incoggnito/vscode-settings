"""Scaffolding template for Python packages."""

"""Bigtoolbox inculding atoolbox and supports extra file types"""

import logging

from atoolbox import (
    BaseFile,
    FileHandler,
    JsonFile,
    TextFile,
    UffFile,
)
from .polyfile import Polyfile


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

logger.info("Package loaded")

__author__ = "Andreas Hofer"
__version__ = "0.0.1"
