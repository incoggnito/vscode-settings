"""Bigtoolbox inculding atoolbox and supports extra file types"""

import logging

from atoolbox import (
    BaseFile,
    FileHandler,
    JsonFile,
    TextFile,
    UffFile,
)
from sqldb import SQLite3Code
from .pridbfile import PridbFile
from .tradbfile import TradbFile
from .trfdbfile import TrfdbFile
from .utils import match_time_to_trai, modify_raw_data_for_features

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

logger.info("Package loaded")

__author__ = "Andreas Hofer"
__version__ = "0.0.1"
