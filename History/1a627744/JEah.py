"""Handle HDF files in a basic way"""

import logging
from pathlib import PurePath

import pandas as pd
import h5py

from .utils import BaseFile
from typing import Dict

LOGGER = logging.getLogger(__name__)


class HdfFile(BaseFile):
    """Special Operations on HDF files"""

    def __init__(self, file_obj: PurePath):
        """Inherit all attributes and methods from the _File Class"""
        super().__init__(file_obj)
        self._check_filetypes((".hdf", ".h5"))
        self.data: pd.DataFrame = pd.DataFrame()

    def get_groups(self) -> None:

        with h5py.File(self.path, "r") as f:
            self.groups = list(f.keys())

    def read(self, project: str = "PyTables", key: str = "", **kwargs: Dict) -> pd.DataFrame:
        """Load a HDF file.

        Returns: A DataFrame

        """
        if project == "PyTables":
            self.data = pd.read_hdf(self.path, **kwargs)
        elif project == "h5py":
            if len(key) == 0:
                LOGGER.warning("If using h5py you have to specify the key of the group to read in.")
                LOGGER.warning("You can get it with the get_groups method.")
            with h5py.File(self.path, "r") as f:
                self.data = f[key]
        return self.data

    def write(self, content: pd.DataFrame) -> None:
        """Save a content to a HDF file.

        Args:
            content: A DataFrame Content

        Returns:None

        """
        raise NotImplementedError
