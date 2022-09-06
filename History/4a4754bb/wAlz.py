import logging
import re
from tracemalloc import start

import pandas as pd
from atoolbox import FileHandler
from datetime import datetime
from tabulate import tabulate

from restapi import AnueTimesheet

KIMAI_PRJ_ACT_ID = {"G": [55, 315], "W": [22, 317], "K": [21, 62], "U": [8, 160], "S": [24, 316], "E": [25, 319]}
LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":

    f = FileHandler("lb.pdf", subdir="data")
    pdf_text = f.read()

    y = 2022
    m = 8
    user = 3

    result = []
    for line in pdf_text.split("\n"):
        d = {}
        if re.match(r"\d{2}\s[M|T|W|F]*"):
            words = line.split()
            d = int(words[0])
            if re.match(r"\d{2}:d{\2}", words[2]):
                start_time = words[2]
                if re.match(r"\d{2}:d{\2}", words[3]):
                    end_time = words[3]
                    activity = [473, 297]
            elif re.match(r"^\d+$", words[2]):
                activity_search_term = words[2]
                if re.match(r"\d{2}:d{\2}", words[3]):
                    start_time = words[3]
                if re.match(r"\d{2}:d{\2}", words[4]):
                    end_time = words[4]
            elif re.match(r"^[G|W|U|S|K|E]$", words[2]):
                activity = KIMAI_PRJ_ACT_ID[words[2]]
            else:
                LOGGER.warning("Can't parse the text information")

            try:
                s = start_time.split(":")
                e = end_time.split(":")
                d["begin"] = datetime(y, m, d, int(s[0]), int(s[1]))
                d["end"] = datetime(y, m, d, int(s[0]), int(s[1]))
                d["project"] = activity[0]
                d["activity"] = activity[1]
                d["user"] = 3
            except:
                LOGGER.warning("No valid kimai entry!")

    ts = AnueTimesheet()

    df = pd.read_excel("lb.xlsx", index_col=0, header=0)
    print(tabulate(df))
