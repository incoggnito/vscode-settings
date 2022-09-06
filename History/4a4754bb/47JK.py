import logging
import re
from datetime import datetime

import pandas as pd
from atoolbox import FileHandler

from restapi import AnueTimesheet, KimaiAPI


LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    api = KimaiAPI()
    # TODO Read excel or pdf
    f = FileHandler("lb.pdf", subdir="data")
    pdf_text = f.read()
    data = pdftext2json(pdf_text, 3, 2022, 7)
    df = pd.DataFrame(data)
    timesheets = [AnueTimesheet(d) for d in data]
