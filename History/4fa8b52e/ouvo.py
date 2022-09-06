import asyncio
import logging
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from sqlite3.dbapi2 import IntegrityError
from typing import Dict

import numpy as np
import vallenae as vae
from vallendb import PridbFile, TradbFile
from vallendb.utils import (
    datetime_str,
    generate_guid,
    get_ae_params,
    get_tr_params,
    hit_from_tra,
)

from fyrsonic import measurement
from fyrsonic.opcua_clients.get_configuration import get_config
from fyrsonic.opcua_servers.conditionWave import Features, Label, Output

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("opcua database writing")


# @log_exception(logger) #TODO needed?
async def save_pridb(
    queue: asyncio.Queue, pridbfile: PridbFile, config: Dict
) -> None:  # TODO Lukas result data type  TestResult
    """[summary]

    Args:
        result (TestResult): [description]
        pridbfile (PridbFile): to write the data in
    """
    # TODO config (Dict): measurement configuration von Server lesen?
    # filename = _generate_filename(result)

    # TODO performance isssues
    # TODO keine direkte Fehlermeldung, wenn die Datenbanken schon existieren, aber beim schreibprozess kommt es dann zu einem Fehler!

    _logger.info(f"Starting to write to {pridbfile.path}")

    # global unique identifier > sqlite > datanbanken nicht verknüpfbar
    # fileid wird einfach generiert > reference id ist identifier von pridb

    pridbfile.determine_write_ae_params(config)
    meas_start = datetime.now()
    pridbfile.write_start_markers(meas_start)
    time = 0.0
    while True:
        # get output from queue
        output: Output = (
            await queue.get()
        )  # TODO output is always only one measurement block, or?
        queue.task_done()
        print(
            f"Read from queue: Channel: {output.channel}, RMS: {output.features.rms}, Crest: {output.features.crest}, Result: {output.result}"
        )

        # for trai, signal in enumerate(output.data, 1):  # result.signals
        # samples = len(signal)
        tra = vae.io.TraRecord(
            time=time,
            channel=1,  # result.channel,
            param_id=1 + 1,  # result.channel + 1,
            pretrigger=0,
            threshold=1e-6,  # 0 dB(AE)
            samplerate=config["Samplefrequency"],  # result.samplerate,
            samples=config["Blocksize"],  # samples,
            data_format=2,
            data=np.random.rand(int(config["Blocksize"])),  # signal, #TODO ERSETZEN!!
            # trai=trai,
        )
        time += float(
            config["Blocksize"] / config["Samplefrequency"]
        )  # float(samples) / result.samplerate

        try:
            hit = hit_from_tra(tra)
        except Exception as e:
            _logger.error("Error during feature extraction:", e)

        try:
            pridbfile.pridb.write_hit(hit)
        except Exception as e:
            _logger.error("Error writing to pridb/tradb:", e)


# async def main(path: Path, filename: str) -> None:
#     """Launch asyncio.Queue and OPC UA client"""
#     config = await get_config()  # TODO check the asyncio theory (correct using?)
#     queue: asyncio.Queue = asyncio.Queue()
#     await asyncio.gather(_save_as_pridb_tradb(queue, path, filename, config)
#     )

# if __name__=="__main__": #TODO implement this
#     path = get_prj_root()
#     path = os.path.join(path, "data\\Measurements")
#     filename = "Test"
#     try:
#         asyncio.run(main(path, filename), debug = True)
