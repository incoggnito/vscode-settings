"""A toolbox for daily business."""

import logging

LOGGER = logging.getLogger(__name__)

from .FileHandler import (
    AudioFile,
    BaseFile,
    ExcelFile,
    FileHandler,
    JsonFile,
    TextFile,
    UffFile,
    PickleFile,
)

__author__ = "Andreas Hofer"
__version__ = "0.6.0"
