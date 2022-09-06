import logging
import re

import pandas as pd
from atoolbox import FileHandler
from datetime import datetime
from tabulate import tabulate

from restapi import AnueTimesheet, KimaiAPI


def parse_anue_pdf_text():
    pass


KIMAI_PRJ_ACT_ID = {"G": [55, 315], "W": [22, 317], "K": [21, 62], "U": [8, 160], "S": [24, 316], "E": [25, 319]}
LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    api = KimaiAPI()
    f = FileHandler("lb.pdf", subdir="data")
    pdf_text = f.read()

    y = 2022
    m = 8
    user = 3

    results = list()
    for line in pdf_text.split("\n"):
        d = dict()
        if re.match(r"\d{2}\s[M|T|W|F]*", line):
            words = line.split()
            d = int(words[0])
            if re.match(r"\d{2}:\d{2}", words[2]):
                start_time = words[2]
                if re.match(r"\d{2}:d{\2}", words[3]):
                    end_time = words[3]
                    activity = [473, 297]
            elif re.match(r"^Schichttausch\s", words[2]):
                activity = [8, 160]
                start_time = "00:00"
                end_time = "23:59"
            else:
                LOGGER.warning("Can't parse the text information")

            try:
                s = start_time.split(":")
                e = end_time.split(":")
                d["begin"] = datetime(y, m, d, int(s[0]), int(s[1]))
                d["end"] = datetime(y, m, d, int(e[0]), int(e[1]))
                d["project"] = activity[0]
                d["activity"] = activity[1]
                d["user"] = 3
                results.append(AnueTimesheet(d))
            except:
                LOGGER.warning("No valid kimai entry!")

    ts = AnueTimesheet()

    df = pd.read_excel("lb.xlsx", index_col=0, header=0)
    print(tabulate(df))
