"""Handle json stuff"""

import pickle
from pathlib import PurePath

from .utils import BaseFile


class PickleFile(BaseFile):
    """Special Operations on json files"""

    def __init__(self, file_obj: PurePath):
        """Inherit all attributes and methods from the _File Class"""
        super().__init__(file_obj)
        self._check_filetypes((".pkl",))
        self.data: dict = dict()

    def read(self) -> dict:
        """Load a json file.

        Returns: A dictionary

        """
        with open(self.path, "rb") as f:
            self.data = dict(pickle.load(f))
            return self.data

    def write(self, content: dict) -> None:
        """Save a json file.

        Args:
            content: A dictionary content

        Returns:None

        """
        with open(self.path, "wb") as f:
            pickle.dump(content, f)
