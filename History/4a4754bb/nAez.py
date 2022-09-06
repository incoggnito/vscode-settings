import logging
import re
from datetime import datetime

import pandas as pd
from atoolbox import FileHandler

from restapi import AnueTimesheet, KimaiAPI


def pdftext2json(pdf_text: str, user: int, year: int, month: int) -> dict:
    results = list()
    for line in pdf_text.split("\n"):
        d = dict()
        if re.match(r"\d{2}\s[M|T|W|F]*", line):
            words = line.split()
            day = int(words[0])
            if re.match(r"\d{2}:\d{2}", words[2]):
                start_time = words[2]
                if re.match(r"\d{2}:\d{2}", words[3]):
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
                d["begin"] = datetime(year, month, day, int(s[0]), int(s[1]))
                d["end"] = datetime(year, month, day, int(e[0]), int(e[1]))
                d["project"] = activity[0]
                d["activity"] = activity[1]
                d["user"] = user
                results.append(d)
            except:
                LOGGER.warning("No valid kimai entry!")
    return results


KIMAI_PRJ_ACT_ID = {"G": [55, 315], "W": [22, 317], "K": [21, 62], "U": [8, 160], "S": [24, 316], "E": [25, 319]}
LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    api = KimaiAPI()
    # TODO Read excel or pdf
    f = FileHandler("lb.pdf", subdir="data")
    pdf_text = f.read()
    data = pdftext2json(pdf_text, 3, 2022, 7)
    df = pd.DataFrame(data)
    timesheets = [AnueTimesheet(d) for d in data]
