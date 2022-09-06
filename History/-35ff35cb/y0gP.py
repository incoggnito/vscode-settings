"""Handle Excel files in basic way"""
import PyPDF2

from pathlib import PurePath

import pandas as pd
from typing import Dict

from .utils import BaseFile


class PdfFile(BaseFile):
    """Special Operations on pdf files"""

    def __init__(self, file_obj: PurePath):
        """Inherit all attributes and methods from the _File Class"""
        super().__init__(file_obj)
        self._check_filetypes((".pdf",))
        self.data: pd.DataFrame = pd.DataFrame()

    def read(self, **kwargs: dict) -> pd.DataFrame:
        pdfFileObj = open(self.path, "rb")
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        self.data = pd.read_csv(self.path, **kwargs)
        return self.data

    def write(self, content: pd.DataFrame, mode: str = "a+", **kwargs: Dict) -> None:
        pass