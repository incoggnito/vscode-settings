"""Bigtoolbox inculding atoolbox and supports extra file types"""

import logging

from atoolbox import (
    BaseFile,
    FileHandler,
    JsonFile,
    SQLite3Code,
    TextFile,
    UffFile,
)

from .BigFileHandler import (
    PridbFile,
    TradbFile,
    TrfdbFile,
    match_time_to_trai,
    modify_raw_data_for_features,
)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

logger.info("Package loaded")

__author__ = "Karl Benkler"
__version__ = "0.0.7"
