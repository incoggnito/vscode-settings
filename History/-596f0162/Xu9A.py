"""Scaffolding template for Python packages."""

import logging

from atoolbox import (
    BaseFile,
    FileHandler,
    JsonFile,
    TextFile,
    UffFile,
)
from .mdffile import MdfFile
from .mf4file import Mf4File

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

logger.info("Package loaded")

__author__ = "Andreas Hofer"
__version__ = "0.0.1"
