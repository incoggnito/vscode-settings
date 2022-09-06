"""create labels for events in the current measurement
"""
import asyncio
import os
from datetime import datetime
from pathlib import Path, PurePath
from typing import List

from atoolbox.FileHandler.jsonfile import JsonFile
from vallendb.pridbfile import PridbFile

from fyrsonic.measurement.configuration import create_config
from fyrsonic.utils.input_handler import select_list_entry

DATA = PurePath(Path(__file__).resolve().parents[3], "data")
MEASUREMENTS = PurePath(DATA, "Measurements")


def read_label_options() -> List:

    label_path = PurePath(DATA, "Settings\\GUI\\Label_options.json")
    labelfile = JsonFile(file_obj=label_path)
    labels = labelfile.read()
    labelsList = list(labels.keys())
    return labelsList


async def label_in_pridb(pridbfile: PridbFile, labelsList: List) -> None:
    message = "Select a label:"
    while True:
        inp = await select_list_entry(message, labelsList)
        timestamp = datetime.now()
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[
            :-3
        ]  # milliseconds should be enough (the user delay should be higher)
        label_value = f"{time_str}\t{inp}"  # \t as deliminter
        pridbfile.write_label(label_value, timestamp)


if __name__ == "__main__":

    settings = PurePath(DATA, "Settings\\measurement\\ConditionWave_settings.json")
    cW_options = PurePath(DATA, "Settings\\measurement\\ConditionWave_options.json")
    if not os.path.exists(MEASUREMENTS):
        os.makedirs(MEASUREMENTS)
    labelsList = read_label_options()
    config = asyncio.run(create_config(cW_options, settings))
    # TODO use measurement folder creation
    pridb_path = PurePath(MEASUREMENTS, "Test_User_Label.pridb")
    pridbfile = PridbFile(pridb_path, config["Datastream 1"], "rwc")
    try:
        asyncio.run(label_in_pridb(pridbfile, labelsList))
    except KeyboardInterrupt:
        print("Closing User label interface")
