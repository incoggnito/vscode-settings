"""
interacts with the conditionWave over tcp/ip and creates and OPC UA Server
Skeleton pipeline with data acquisition, feature extraction, classification and OPC UA output.

The pipeline can run on an external PC or directly on the conditionWave (using the IP 127.0.0.1).
Please contact Vallen System <software@vallen.de> for more details.
"""

# [ ] TODO add logging of the temperature (of the device) -> get status
# [ ] TODO add logging of errors? get error

# [ ] TODO add switch to new db after midnight (in 24/7 measurement mode)

import argparse
import asyncio
import logging

from datetime import datetime
from pathlib import PurePath

import numpy as np
import pandas as pd
import vallenae as vae
from vallendb import FileHandler, PridbFile, TradbFile  # , setup_logging
from waveline import ConditionWave

LOGGER = (
    logging.getLogger()
)  # get the root logger -> duplicate entries (child entries and parent entries)
LOGGER.setLevel(logging.INFO)

# [ ] TODO fix the errors if stoping with STRG+C


def read_config(configfile: PurePath) -> pd.DataFrame:
    f = FileHandler(filename=configfile.name, wkd=configfile.parent)
    config = f.current_file.read()
    config_df = pd.DataFrame.from_dict(config)
    config_df.loc[0, "Device"] = "[-]"  # correct the reading
    return config_df


async def channel_acquisition(
    stream,
    channel: int,
    samplefrequency: int,
    blocksize: int,
    tradb_file: TradbFile,
    pridb_file: PridbFile,
    trai: int = 1,
    trai_increment: int = 1,
    time: float = 0.0,
) -> None:
    # blocktime_step = blocksize / samplefrequency
    # [ ] REVIEW use the timestamp of the datastream?
    async for time, data in stream:
        # [ ] TODO use the timestamp from the device (calculation of the time delta to starttimepoint needed?)
        # [ ] TODO the current trai increment, can cause geps in the trai (different blocksizes, trais currently coupled to the channel number)
        # [ ] TODO Vallen: trai has no gaps!
        write_transientdata(
            data,
            samplefrequency,
            blocksize,
            channel,
            tradb_file,
            time,
            trai,
        )
        write_hit(
            data,
            samplefrequency,
            blocksize,
            channel,
            pridb_file,
            time,
            trai,
        )
        # every stream has it own first trai and the same trai_increment
        # stream of channel 1: first trai = 1, second trai = 3, ...
        # stream of channel 2: first trai = 2, second trai = 4, ...
        # if there is only one stream of one channel: first trai = 1, second trai = 2, ...
        # time += blocktime_step
        trai += trai_increment

        # TODO Publish comprimated data to mqtt


async def pipeline(
    ip: str,
    stream_config: pd.DataFrame,
    tradbfile: TradbFile,
    pridbfile: PridbFile,
    trai: int = 1,
    time: float = 0.0,
):
    """Pipeline: data acquisition, feature extraction and classification.

    Args:
        ip (str): IP-Adress of the conditionWave
        channel (int): [description]
        queue (asyncio.Queue): [description]
        fyr_config (Dict): [description]
    """

    # [x] TODO initializing all channels seperate. setting all channels at once, if the have the same settings would be more readabily

    async with ConditionWave(ip) as cw:
        LOGGER.info(await cw.get_info())
        # skipping the first line (contains the units)
        for _, config_row in stream_config.loc[1:].iterrows():
            channel = int(config_row["Channel"])
            LOGGER.debug(
                f"Range: {config_row['Range']} , Type: {type(config_row['Range'])}"
            )
            await cw.set_range(channel, range_volts=float(config_row["Range"]))

            LOGGER.debug(
                f"Decimation factor: {int(cw.MAX_SAMPLERATE / config_row['Samplefrequency'])} , Type: {type(int(cw.MAX_SAMPLERATE / config_row['Samplefrequency']))}"
            )
            await cw.set_tr_decimation(
                channel, factor=int(cw.MAX_SAMPLERATE / config_row["Samplefrequency"])
            )
            await cw.set_filter(
                channel,
                highpass=config_row["Highpass Filter Cutoff Frequency"],
                lowpass=config_row["Lowpass Filter Cutoff Frequency"],
                order=config_row["Filterorder"],
            )
            LOGGER.info(await cw.get_setup(channel))
        # [ ] TODO read the adc2uv from the conditionWave?
        with tradbfile(mode="rw", compression=True) as tradb, pridbfile(
            mode="rw"
        ) as pridb:
            datetime_start = datetime.now()
            await cw.start_acquisition()
            LOGGER.info("Start to measure")
            pridb.write_start_markers(datetime_start)
            # the measurement data from the condidtion wave is in volts (sure in case of range of 0.05V)
            streams = []
            trai_increment = stream_config.shape[0] - 1  # number of channels
            for _, config_row in stream_config.loc[1:].iterrows():
                channel = int(config_row["Channel"])
                streams.append(
                    # asyncio.shield(
                    channel_acquisition(
                        cw.stream(
                            channel,
                            config_row["Blocksize"],  # start=datetime_start
                        ),
                        channel,
                        config_row["Samplefrequency"],
                        config_row["Blocksize"],
                        tradb,
                        pridb,
                        trai,
                        trai_increment,
                        time,
                    )
                    # )
                )
                trai += 1

            try:
                await asyncio.gather(*streams)
            except KeyboardInterrupt:
                LOGGER.info("Catched the keyboard interrupt in pipeline.")
                pass
            finally:
                await cw.stop_acquisition()
                # using here the Samplefrequency of the first channel for the stop markers
                pridb.write_stop_marker(stream_config.loc[1, "Samplefrequency"])


def write_transientdata(
    data: np.ndarray,
    samplefrequency: int,
    blocksize: int,
    channel: int,
    tradb_file: TradbFile,
    time: float = 0.0,
    trai: int = 0,
) -> None:
    """wirtes the transient measurement data to a tradb

    Args:
        data (np.ndarray): measurement data
        stream_config (dict): configuration of the stream to write
        tradb_file (TradbFile): tradb to write in
        trai (int, optional): transient index. Defaults to 1.
    """
    # trai += 1  # TODO workaround to increment the trai for every entry, time for two channel data blocks the same!
    # [ ] TODO currently when starting a new measurement and appending data to existing pridb/tradb the trai is the same then the last trai of the previous mesurement
    try:
        tra_record = vae.io.TraRecord(
            time=time,
            channel=channel,
            param_id=channel + 1,
            pretrigger=0,
            threshold=0,
            samplerate=samplefrequency,
            samples=blocksize,
            data=data,
            trai=trai,
        )

        tradb_file.write(tra_record)
    except KeyboardInterrupt:
        raise


def write_hit(
    data: np.ndarray,
    samplefrequency: int,
    blocksize: int,
    channel: int,
    pridb_file: PridbFile,
    time: float = 0.0,
    trai: int = 0,
) -> None:
    """wirtes the transient measurement data to a tradb

    Args:
        data (np.ndarray): measurement data
        stream_config (dict): configuration of the stream to write
        tradb_file (TradbFile): tradb to write in
        trai (int, optional): transient index. Defaults to 1.
    """
    # trai += 1  # [ ] HACK: pridb: the trai is for one measurement block for all channels the same, but the time is not the same!
    # -> Vallen GUI: TRAI is unique, time is for one block for all channels the same
    # [ ] HACK: pridb: time completly wrong? timeline in pridb: trai 2-4 ch 1 -> with blocktimestep -> blocktimestep going on trai 2-3 ch 2 ->
    # time completly messed up
    # [ ] HACK: tradb: time and trai for one block for both channels the same -> looks better -> vallen -> time for one block for all channels the same
    # but the trai is unique!
    try:
        amplitude = vae.features.acoustic_emission.peak_amplitude(
            data
        )  # vaspy.feature.acoustic_emission.hit_peak(data) # [ ] Review which peak implemtation to use
        energy = vae.features.acoustic_emission.energy(
            data, samplefrequency
        )  # vaspy.feature.acoustic_emission.hit_energy(data) # [ ] Review which peak implemtation to use
        rms = vae.features.acoustic_emission.rms(data)  # vaspy.feature.basic.rms(data)
        hit_record = vae.io.HitRecord(
            time,
            channel,
            3,
            amplitude=amplitude,
            duration=blocksize
            / samplefrequency,  # [ ]  workaround for a bugfix from Lukas?
            energy=energy,
            rms=rms,
            signal_strength=0.0,
            trai=trai,
        )

        pridb_file.write(hit_record, samplefrequency, blocksize)
    except KeyboardInterrupt:
        raise


async def start_measurement(
    ip: str, outputfilepath: PurePath, config: pd.DataFrame, append: bool = False
) -> None:

    # detected_devices = ConditionWave.discover()
    # if not detected_devices:
    #     LOGGER.error(
    #         "No device found! Try to disconnect and reconnect the network cables."
    #     )
    #     raise ConnectionError
    # else:
    #     LOGGER.info(f"Connecting to: {detected_devices[0]}")
    #     ip = detected_devices[0]  # use first device

    # ip = "192.168.102.164"  # using the zyxel switch in Seefeld
    # ip = "192.168.88.253"  # static ip adress if you use a seperate network (prefer the above line), HEXAPOE

    f = FileHandler(filename=outputfilepath.name, wkd=outputfilepath.parent)
    tradbfile = f.current_file
    f.set_file(f"{outputfilepath.stem}.pridb")
    pridbfile = f.current_file

    # [x] TODO use here with statement to open and close tradb
    with tradbfile(mode="rwc", compression=True) as tradb, pridbfile(
        mode="rwc"
    ) as pridb:
        if not append:
            tradb.create(config)
            pridb.create(config)
            LOGGER.info("Tradbfile and Pridbfile created.")
            trai_last = 1
            t_last = 0.0
        else:
            (t_last, trai_last) = tradb.get_last_time_trai()
            LOGGER.info(f"Last time point in existing file: {t_last}")
            LOGGER.info(f"Last TRAI in existing file: {trai_last}")
            trai_last += 1

        try:
            await pipeline(ip, config, tradb, pridb, trai_last, t_last)
        except KeyboardInterrupt:
            LOGGER.info("Catched Keyboard interrupt in start_measurement.")
            pass

    # TODO copy SETid two TRAI (only one trai value) ??


if __name__ == "__main__":
    now = datetime.now()
    now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--outputfile",
        default=f"data/Measurements/Test_{now_str}.tradb",
        type=str,
        help="The path to the outputfile, e.g.: data/Measurements/Test.tradb",
    )
    parser.add_argument(
        "-c",
        "--configfile",
        default="data/settings/measurement/ConditionWave_settings.json",
        type=str,
        help="The path to the configfile, e.g.: data/settings/measurement/ConditionWave_settings.json",
    )
    parser.add_argument(
        "-i",
        "--ipaddress",
        default="192.168.105.97",
        type=str,
        help="The ip address of the measurement device, e.g.: 192.168.105.97",
    )
    args = parser.parse_args()
    args.outputfile = args.outputfile.strip()
    args.configfile = args.configfile.strip()
    outputfile = PurePath(args.outputfile)
    configfile = PurePath(args.configfile)
    ipadress = args.ipaddress

    LOGGER.debug(f"{configfile}")
    if not configfile.is_absolute():
        f = FileHandler(filename=configfile.name, subdir=list(configfile.parts[:-1]))
    else:
        f = FileHandler(filename=configfile.name, wkd=configfile.parent)
    LOGGER.debug(f"{f.current_file.path}")
    config = read_config(f.current_file.path)
    LOGGER.debug(f"{outputfile}")
    if not outputfile.is_absolute():
        f = FileHandler(filename=outputfile.name, subdir=list(outputfile.parts[:-1]))
    else:
        f = FileHandler(filename=outputfile.name, wkd=outputfile.parent)
    if not f.exist_path():
        f.create_folders()
    append = False
    if f.exist_file():
        LOGGER.info(
            "The measurement databases are already existing. Going to append the data."
        )
        append = True
    try:
        LOGGER.info("Starting measurement interface")
        # [ ] TODO handle the RuntimeError: Event loop is closed
        asyncio.run(start_measurement(ipadress, f.current_file.path, config, append))

    except ConnectionError:
        LOGGER.info("No measurement data written.")
    except KeyboardInterrupt:
        LOGGER.info("KeyboardInterrupt catched at the outisde of asyncio run.")
    finally:
        stop = datetime.now()
        stop_str = stop.strftime("%Y_%m_%d_%H_%M_%S.%f")
        f = FileHandler(filename=outputfile.name, wkd=outputfile.parent)
        tradbfile = f.current_file
        with tradbfile(mode="rw") as tradb:
            LOGGER.info("Closing measurement data file.")
        LOGGER.info("Measurement completed")
        LOGGER.debug(f"Measurement stopped at: {stop_str}")
    LOGGER.info("Measurement interface closed.")
