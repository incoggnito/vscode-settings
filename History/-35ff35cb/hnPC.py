"""Handle Excel files in basic way"""

from pathlib import PurePath, Path

import pandas as pd
from typing import Dict, List, Union

from .utils import BaseFile


class CsvFile(BaseFile):
    """Special Operations on csv files"""

    def __init__(self, file_obj: PurePath):
        """Inherit all attributes and methods from the _File Class"""
        super().__init__(file_obj)
        self._check_filetypes((".csv",))
        self.data: pd.DataFrame = pd.DataFrame()

    def read(self, **kwargs: dict) -> pd.DataFrame:
        """Load a csv file.

        Args:
            kwargs: passed to pandas.read_csv()

        Returns: pd.DataFrame containing the read data

        """
        self.data = pd.read_csv(self.path, **kwargs)
        return self.data

    def write(self, content: pd.DataFrame, mode: str = "a+", **kwargs: Dict) -> None:
        """Save a excel file.

        Args:
            content (pandas DataFrame): data to write in the csv file
            mode (str): "a+": appending data to existing file or create file, else overwrite or create file.
                Defaults to a+.
            **kwargs: (Dict): passed to pandas.to_csv()

        Returns:None

        """
        # [ ] Review: file exists is a method of filehandler -> not accesible by fileclasses?
        content.to_csv(self.path, mode=mode, **kwargs)