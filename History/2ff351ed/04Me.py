"""Process to calculate all features and write a trfdb
Should be executed parallel to a measurment (with tradb generation) or after the measurement
see also: pytiepiesql/measurement/trfdb_writer.py
"""
import argparse
import logging
import time
from datetime import datetime
from pathlib import PurePath
from typing import Dict, List, Optional

import pandas as pd
from vallendb import FileHandler
from vallendb.utils import (
    feature_live_generation,
    read_acq_settings,
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel("DEBUG")


def trfdb_writing(
    inputfile: PurePath,
    acq_settings: pd.DataFrame,
    features: List[str] = ["All"],
    append: bool = False,
    trai_start: int = 1,
    write_trfdb: bool = True,
    mqtt_publish: bool = False,
    mqtt_config: Optional[Dict] = None,
    mqtt_topic: str = "feature",
) -> None:

    if write_trfdb:
        # [ ] TODO evtl. MultiProcessing notwendig hängt bisschen hinterher
        filename = inputfile.stem
        suffix = ".trfdb"
        f = FileHandler(wkd=inputfile.parent)
        f.set_file(f"{filename}{suffix}")
        trfdbfile = f.current_file
        if f.exist_file() and append:
            LOGGER.info(f"Appending to existing trfdbfile: {trfdbfile.path}")
            with trfdbfile(mode="ro") as trfdb:
                trai_start = trfdb.get_last_trai() + 1
        elif f.exist_file() and not append:
            now = datetime.now()
            now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
            f.set_file(f"{filename}_{now_str}{suffix}")
            trfdbfile = f.current_file
            with trfdbfile(mode="rwc") as trfdb:
                trfdb.create(acq_settings)
                LOGGER.info(f"Trfdb file created: {trfdbfile.path}")
        else:
            with trfdbfile(mode="rwc") as trfdb:
                trfdb.create(acq_settings)
                LOGGER.info(f"Trfdb file created: {trfdbfile.path}")

    feature_live_generation(
        inputfile,
        trai_start,
        feature_selection=features,
        write_trfdb=write_trfdb,
        mqtt_publish=mqtt_publish,
        mqtt_config=mqtt_config,
        mqtt_topic=mqtt_topic,
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--inputfile",
        default="data/Measurements/Test.tradb",
        type=str,
        help="The path to the inputfile, e.g.: data/Measurements/Test.tradb . The data of that file is used for the feature calculation. The trfdb-file gets the same name. The measurement configuration is read from that file.",
    )
    # get a complete list of all available features at vaspy.feature.activate_features
    parser.add_argument(
        "-f",
        "--features",
        default="RMS, Peak_Amplitude, HFC",
        type=str,
        help="List of features to calculate. e.g: 'All' or 'RMS, Peak_Amplitude, HFC'. Possible features are: 'Mean, Hit_Peak, Hit_Energy,RMS, Peak_Amplitude, Crest_Factor, K_Factor, Impulse_Factor, Margin_Factor, Shape_Factor, Clearance_Factor, Zero_Crossing_Rate, Spectral_Peak, Spectral_Centroid, Spectral_Spread, HFC, Spectral_Rolloff, Spectral_Flatness, Kurtosis, FFT_Mean",
    )
    args = parser.parse_args()
    args.inputfile = args.inputfile.strip()
    inputfile = PurePath(args.inputfile)

    LOGGER.debug(f"Passed features: {args.features}")
    features = args.features.split(",")
    features = list(map(str.strip, features))

    LOGGER.debug(f"Got following tradbfile: {inputfile}")
    LOGGER.debug(f"Got following features: {features}")

    if not inputfile.is_absolute():
        f = FileHandler(filename=inputfile.name, subdir=list(inputfile.parts[:-1]))
    else:
        f = FileHandler(filename=inputfile.name, wkd=inputfile.parent)
    inputfile = f.current_file

    if not f.exist_file():
        # [ ] Review duration
        time.sleep(2)
    if not f.exist_file():
        raise FileNotFoundError(
            f"The passed tradbfile: {inputfile.path} does not exist!"
        )

    acq_settings = read_acq_settings(inputfile.path)
    try:
        LOGGER.info("Starting trfdb writer")
        trfdb_writing(
            inputfile.path,
            acq_settings,
            features,
            append=True,
            trai_start=1,
            write_trfdb=False,
            mqtt_publish=True,
            mqtt_config={"broker_ip": "192.168.102.109", "broker_port": 1883},
        )
    except KeyboardInterrupt:
        pass
    finally:
        # needed to process the last samples
        trfdb_writing(inputfile.path, acq_settings, features, append=True)
        stop = datetime.now()
        stop_str = stop.strftime("%Y_%m_%d_%H_%M_%S.%f")
        LOGGER.debug(f"Trfdb writer stopped at: {stop_str}")
