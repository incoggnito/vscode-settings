"""Handle json stuff"""

from pathlib import PurePath

import pandas as pd
from asammdf import MDF

from .utils import BaseFile


class MdfFile(BaseFile):
    """Special Operations on json files"""

    def __init__(self, file_obj: PurePath):
        """Inherit all attributes and methods from the _File Class"""
        super().__init__(file_obj)
        self._check_filetypes((".mf4",))
        self.data: dict = dict()

    def read(self) -> pd.DataFrame:
        """Load a mf4 file.
        Returns: A pandas DataFrame

        """
        with MDF(self.path) as mdf:
            mdf = MDF(self.path)
            self.data = mdf.to_dataframe()
            self.header = mdf.header

    def write(self, content: dict) -> None:
        """Save a  file.

        Args:
            content: A dictionary content

        Returns:None

        """
        ...
