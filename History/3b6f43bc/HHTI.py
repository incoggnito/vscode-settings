"""A toolbox for daily business."""

import logging
LOGGER = logging.getLogger(__name__)
try: 
    __import__(win32com)
    from .EmailHandler import Mail
    from .FileHandler import PolyFile, read_coherence, read_fft, read_frf
except ImportError:
    LOGGER.info("On a linux machine. The Emailhandler is not available.")
except NameError:
    LOGGER.info("NameError: On a linux machine. EmailHandler only available for Windows machines.")
from .FileHandler import (
    AudioFile,
    BaseFile,
    ExcelFile,
    FileHandler,
    HdfFile,
    JsonFile,
    TextFile,
    UffFile,
)
from .SQLHandler import NVHBrake, SQLite3Code

__author__ = "Andreas Hofer"
__version__ = "0.6.0"
