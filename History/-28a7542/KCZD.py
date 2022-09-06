"""
interacts with the conditionWave over tcp/ip and creates and OPC UA Server
Skeleton pipeline with data acquisition, feature extraction, classification and OPC UA output.

The pipeline can run on an external PC or directly on the conditionWave (using the IP 127.0.0.1).
Please contact Vallen System <software@vallen.de> for more details.
"""

import asyncio
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePath
from typing import Dict, List

import numpy as np
import vallenae as vae
import vaspy.feature.calculation
from vallendb.utils import setup_logging, TradbFile
from waveline import ConditionWave

from fyrsonic.opcua_servers.utils import (
    initialize_opcua_sever,
    measurement_config_to_opcua,
    update_variable,
)

DATA = PurePath(Path(__file__).resolve().parents[3], "data")
MEASUREMENTS = PurePath(DATA, "Measurements")
OPCUA = PurePath(DATA, "Settings\\opcua")
CHANNELS = 2

# logging.basicConfig(level=logging.INFO)
logger = setup_logging()
logger.info(f"Starting to execute{__name__}")


@dataclass
class Features:
    """Feature vector."""

    rms: float
    crest: float


@dataclass
class Label:
    """Label of the data"""

    label: str


@dataclass
class Output:
    """Container for OPC UA outputs."""

    channel: int
    features: Features
    label: Label


def get_range(range: str) -> float:
    """Range as string to float"""
    if range == "50 mV":
        return 0.05
    elif range == "5 V":
        return 5.0
    else:
        raise NotImplementedError


# def extract_features(signal: np.ndarray) -> Features:
#     """Feature extraction."""
#     peak = np.max(np.abs(signal))
#     rms = np.sqrt(np.mean(signal ** 2))
#     return Features(
#         rms=rms,
#         crest=peak / rms,
#     )


def classify(rms: float) -> Label:
    """Inference based on feature vector, just a placeholder for your logic/model."""
    if rms >= 1e-5:  # >= 1 mV #TODO add here simple logic to classify
        return Label(label="RMS höher als 1e-5")
    return Label(label="RMS in Ordnung")


# [ ] TODO check if now the created tradbs are right!


async def channel_acquisition(
    stream,
    channel: int,
    stream_config: Dict,
    tradb_file: TradbFile,
    queue: asyncio.Queue,
    feature_selection: List,
) -> None:
    trai = channel  # first trai = channel number
    blocktime_step = stream_config["Blocksize"] / stream_config["Samplefrequency"]
    blocktime = blocktime_step
    async for timestamp, data in stream:
        print(f"Channel {channel}, {timestamp}, {len(data)} samples")
        write_transientdata(data, stream_config, channel, tradb_file, blocktime, trai)
        trai += CHANNELS  # the channels alter in the same way
        with ThreadPoolExecutor() as pool:
            loop = asyncio.get_event_loop()
            # read streaming data in blocks
            # execute (longer) blocking operations in the thread pool -> don't block event loop
            # await loop.run_in_executor(
            #     pool,
            # write_transientdata,
            # data,
            # stream_config,
            # channel,
            # tradb_file,
            # trai,
            # )
            blocktime += blocktime_step  # increment the blocktime here to have the same time for both channels
            features = await loop.run_in_executor(
                pool,
                determine_features,
                data,
                stream_config,
                feature_selection,
            )
            # features = await loop.run_in_executor(pool, extract_features, data)
            label = await loop.run_in_executor(pool, classify, features["RMS"])
        # print(f"Rms:{features.rms} , Crest: {features.crest}, Label: {label.label}")
        # queue.put_nowait(Output(channel, features=features, label=label))
        queue.put_nowait(
            (channel, blocktime, features["RMS"], features["Crest_Factor"], label)
        )


async def pipeline(
    ip: str,
    queue: asyncio.Queue,
    stream_config: Dict,
    tradb_file: TradbFile,
    feature_selection: List,
):
    """Pipeline: data acquisition, feature extraction and classification.

    Args:
        ip (str): IP-Adress of the conditionWave
        channel (int): [description]
        queue (asyncio.Queue): [description]
        fyr_config (Dict): [description]
    """

    samplefrequency = stream_config["Samplefrequency"]
    blocksize = stream_config["Blocksize"]
    range = get_range(stream_config["Range"])
    highpass = stream_config["Filter-LowerLimit"]
    lowpass = stream_config["Filter-UpperLimit"]
    order = stream_config["Filter-Order"]

    # TODO now all channels same settings

    async with ConditionWave(ip) as cw:
        logger.info(await cw.get_info())
        await cw.set_range(0, range_volts=range)
        await cw.set_decimation(0, factor=int(cw.MAX_SAMPLERATE / samplefrequency))
        await cw.set_filter(0, highpass=highpass, lowpass=lowpass, order=order)
        datetime_start = datetime.now()
        await cw.start_acquisition()
        logger.info("Start to measure")

        streams = [
            channel_acquisition(
                cw.stream(channel, blocksize, start=datetime_start),
                channel,
                stream_config,
                tradb_file,
                queue,
                feature_selection,
            )
            for channel in (1, 2)
        ]

        try:
            # async handling of the streams -> trai is the same!
            await asyncio.gather(*streams)
        finally:
            await cw.stop_acquisition()

        #             # print(timestamp, features, result)
        #             # push output to queue
        #             # TODO handle data y
        #             queue.put_nowait(Output(ch, features=features, label=label))
        # # TODO write transient data to tradb
        # # TODO write features to trfdb
        # # TODO maybe create pridb if necessary

        # await cw.stop_acquisition()


def write_transientdata(
    data: np.ndarray,
    stream_config: dict,
    channel: int,
    tradb_file: TradbFile,
    time: int,
    trai: int = 0,
) -> None:
    """writes the transient measurement data to a tradb

    Args:
        data (np.ndarray): measurement data
        stream_config (dict): configuration of the stream to write
        tradb_file (TradbFile): tradb to write in
        trai (int, optional): transient index. Defaults to 1.
    """
    blocksize = stream_config["Blocksize"]
    fs = stream_config["Samplefrequency"]
    # ch = stream_config["Channel"]
    trai += 1  # TODO workaround to increment the trai for every entry, time for two channel data blocks the same!
    tra_record = vae.io.TraRecord(
        time=time,
        channel=channel,
        param_id=channel + 1,
        pretrigger=0,
        threshold=0,
        samplerate=fs,
        samples=blocksize,
        data_format=2,
        data=data,
        trai=trai,
    )

    tradb_file.write(tra_record)


def determine_features(
    data: np.ndarray,
    stream_config: dict,
    feature_selection: List = ["All"],
) -> Dict:
    features = vaspy.feature.calculation.feature_calculation(
        data,
        stream_config["Samplefrequency"],
        stream_config["Pretrigger"],
        feature_selection=feature_selection,
    )
    return features


async def publish_data(
    queue: asyncio.Queue, server_config: Dict, opcua_folders: Dict
) -> None:
    """Publish measurement data (only features, labels, config) as opcua server

    Args:
        queue (asyncio.Queue): Queue with the measurement data
        server_config (Dict): configuration of the opcua-Server to publish the data
        opcua_folders (Dict): configuration of the folders and Nodes of the opcua_Server
    """
    async with server_config["server"]:
        while True:
            # output: Output = await queue.get()  # wait for data
            (
                channel,
                blocktime,
                rms,
                crest,
                label,
            ) = await queue.get()
            queue.task_done()
            await update_variable(
                opcua_folders["channel"]["Variables"]["Ch"]["NodeID"],
                # str(output.channel),  # TODO workout, that this variable is a int
                str(channel),
            )
            await update_variable(
                opcua_folders["features"]["Variables"]["RMS"]["NodeID"],
                # float(output.features.rms),
                rms,
            )
            await update_variable(
                opcua_folders["features"]["Variables"]["Crest"]["NodeID"],
                # float(output.features.crest),
                crest,
            )
            await update_variable(
                opcua_folders["label"]["Variables"]["label"]["NodeID"],
                label.label,
            )


async def measurement_processing(
    ip: str,
    config: Dict,
    tradb_file: TradbFile,
    opcua_servers: List,
    opcua_folders_configs: List,
    feature_selection: List,
) -> None:
    """Launch pipeline and OPC UA server."""
    output_queue_Ch1: asyncio.Queue = (
        asyncio.Queue()
    )  # decouple acquisition/processing and io
    # output_queue_Ch2: asyncio.Queue = (
    #    asyncio.Queue()
    # )  # decouple acquisition/processing and io

    for i, server in enumerate(opcua_servers):
        server = await initialize_opcua_sever(server, opcua_folders_configs[i])
    print("OPCUA-Servers ready")
    await asyncio.gather(  # TODO for loop for all servers in this asyncio.gather?
        publish_data(output_queue_Ch1, opcua_servers[0], opcua_folders_configs[0]),
        # opcua_server(
        #     output_queue_Ch2,
        #     "opc.tcp://0.0.0.0:4841",
        #     "conditionWave OPC UA server, Channel 2",
        #     "https://www.conditionWaveCh2.de",
        # ),
        pipeline(
            ip,
            output_queue_Ch1,
            config["Datastream 1"],
            tradb_file,
            feature_selection,
        ),
        # pipeline(ip, 2, output_queue_Ch2),
        # write_databases(output_queue_Ch1, output_queue_Ch2, fyr_config, tradb),
    )


async def start_measurement(filename: str) -> None:

    event_loop = asyncio.get_event_loop()
    asyncio.set_event_loop(event_loop)
    terminal_use = False
    development = True
    DATA = PurePath(Path(__file__).resolve().parents[3], "data")
    MEASUREMENTS = PurePath(DATA, "Measurements")
    OPCUA = PurePath(DATA, "Settings\\opcua")
    feature_selection = [
        "Mean",
        "Hit_Peak",
        "Hit_Risetime",
        "Hit_RA_Value",
        "Hit_ZCR",
        "Hit_Energy",
        "Power_Mean",
        "RMS",
        "Peak_Amplitude",
        "Crest_Factor",
        "K_Factor",
        "Impulse_Factor",
        "Margin_Factor",
        "Shape_Factor",
        "Clearance_Factor",
        "Zero_Crossing_Rate",
        "Spectral_Peak",
        "Spectral_Centroid",
        "Spectral_Spread",
        "HFC",
        "Spectral_Rolloff",
        "Percentile",
        "STD",
        "Skewness",
        "Kurtosis",
        "FFT_Mean",
    ]

    detected_devices = ConditionWave.discover()
    if not detected_devices:
        sys.exit("No device found! Try to disconnect and reconnect the network cables.")
    else:
        ip = detected_devices[0]  # use first device

    # ip = "192.168.102.164"  # using the zyxel switch in Seefeld
    # ip = "192.168.88.253"  # static ip adress if you use a seperate network (prefer the above line), HEXAPOE
    config = {
        "Datastream 1": {
            "Channel": 1,
            "MeasurementMode": "Streaming",
            "Pretrigger": 0,
            "Range": "50 mV",
            "PreamplifierGain": "0 dB",
            "Samplefrequency": 1000000,
            "Filter-LowerLimit": None,
            "Filter-UpperLimit": None,
            "Filter-Order": 8,
            "Blocksize": 65536,
        },
        "Datastream 2": {
            "Channel": 2,
            "MeasurementMode": "Streaming",
            "Pretrigger": 0,
            "Range": "50 mV",
            "PreamplifierGain": "0 dB",
            "Samplefrequency": 1000000,
            "Filter-LowerLimit": None,
            "Filter-UpperLimit": None,
            "Filter-Order": 8,
            "Blocksize": 65536,
        },
    }
    if not os.path.exists(MEASUREMENTS):
        os.makedirs(MEASUREMENTS)

    # options = [
    #     "Manually input the measurement settings",
    #     "Use the measurement settings file?",
    # ]
    # inp = await select_list_entry("Measurement settings:", options)
    # cW_options = PurePath(DATA, "Settings\\measurement\\ConditionWave_options.json")
    # if inp == options[0]:
    #     config = await create_config(cW_options)
    # else:
    #     settings = PurePath(DATA, "Settings\\measurement\\ConditionWave_settings.json")
    #     config = await create_config(cW_options, settings)

    (opcua_servers, opcua_folders_configs) = measurement_config_to_opcua(config)

    # if not development:
    #     file_name = create_output_folder_structure(MEASUREMENTS)
    #     channels = 2
    #     tradb_path = Path(f"{file_name}.tradb")

    # else:
    tradb_path = PurePath(
        Path(__file__).resolve().parents[3], f"data/Measurements/{filename}.tradb"
    )

    # TODO setup the the tradbfile with the config of the first datastream? -> when using two datastreams with different configs, best way two save two pridbs?
    compression = True
    tradb_file = TradbFile(
        tradb_path, config["Datastream 1"], mode="rwc", compression=compression
    )
    print("Tradbfile created.")
    # tradb_file.write_start_lines(
    #     config["Datastream 1"]["Samplefrequency"],
    #     config["Datastream 1"]["Blocksize"],
    #     compression,
    # )

    try:
        await measurement_processing(
            ip,
            config,
            tradb_file,
            opcua_servers,
            opcua_folders_configs,
            feature_selection,
        )
    except KeyboardInterrupt:
        ...
    finally:
        # TODO close database connections
        tradb_file.tradb.close()
        print("Successfully closed all database connections.")

    # TODO copy SETid two TRAI (only one trai value)


if __name__ == "__main__":
    filename = "Test"
    asyncio.run(start_measurement(filename))
