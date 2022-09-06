"""Base File object"""
import logging
import os
import uuid
from datetime import datetime
from functools import wraps
from pathlib import Path, PurePath
from sqlite3 import OperationalError
from time import sleep
from typing import Any, Callable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import sqlalchemy as sa
import vallenae as vae
from atoolbox import FileHandler
from sqldb import SQLite3Code
from vallenae.io.datatypes import TraRecord
from vallenae.io.pridb import PriDatabase
from vaspy.feature.calculation import feature_calculation

LOGGER = logging.getLogger(__name__)
Vaedatabase = Union[vae.io.PriDatabase, vae.io.TraDatabase]

SQLITE3CODE_PATH = PurePath(Path(__file__).resolve().parent, "sqlite3_code")


def get_logfile_path() -> PurePath:
    """Generates the path to the folder containing the log files.
        If the folder not exist, if creats it.

    Returns:
        PurePath: Path to the logs-folder
    """
    f = FileHandler(subdir=["data", "logs"])
    if not os.path.exists(f.fullpath):
        f.create_folders()
    return PurePath(f.fullpath)


def setup_logging() -> logging.Logger:
    """Setting up logging to file

    Returns:
        logging.Logger: logger to write in
    """
    # source:
    # https://pythonhowtoprogram.com/logging-in-python-3-how-to-output-logs-to-file-and-console/
    # [ ] TODO necessary?

    logfile_path = get_logfile_path()

    mylogs = logging.getLogger()  # get the root logger -> duplicate entries (child entries and parent entries)
    mylogs.setLevel(logging.ERROR)

    timestamp = datetime.now()
    timestamp_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    logfile = timestamp_str + "_Logfile.log"  # TODO include in the name of the logfile the script which is logged,
    # maybe: os.path.basename(__file__)
    file_path = PurePath(logfile_path, logfile)

    filelogger = logging.FileHandler(file_path)
    fileformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
    filelogger.setFormatter(fileformat)
    mylogs.addHandler(filelogger)

    # stream = logging.StreamHandler()  # for console output
    # stream.setLevel(logging.INFO)
    # streamformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
    # stream.setFormatter(streamformat)

    return mylogs


def get_adc_microV(range: int) -> float:
    """maps the measurement range to the adc conversion factor: microVolt <-> bit

    Args:
        range (int): measurement range, 50 or 5000 [mV]

    Returns:
        float: adc_microV
    """
    # TODO in this mapping also consider the preamplifier gain!
    adc_microV_map = {"50": 1.66666694444449, "5000": 168.333342100695}
    adc_microV = float(adc_microV_map[str(range)])
    return adc_microV


def get_ae_params(config: pd.DataFrame) -> pd.DataFrame:
    """
    ae_params: ID, SetupID, Chan, ADC_microV, ADC_TE, ADC_SS, PA0_mV
    first line (channel 0) always only zero entries
    ADC_microV, ADC_TE, ADC_SS, PA0_mV depend on the measurement settings
    for informations see: https://cloud.amitronics.net/f/160886
    conversion to μV with the factor <adc2uv> available via the get_setup or get_status command

    Args:
        pridb (Pridatabase): database in which the ae_params should be updated
        config (pd.DataFrame): See read or store_acq_settings

    Returns:
        str: sql command to insert the ae_params into the pridb
    """
    # TODO implement the mapping

    LOGGER.warning(" Get_ae_params is not finally implemented. There maybe errors (2 digit after the dezimal point).")
    # np.float64 needed to avoid rounding error in the later computation
    range_V = config.loc[1:, "Range"].to_numpy(dtype=np.float64)  # from [V] to [microV]
    gain = config.loc[1:, "Preamplifier gain"].to_numpy(dtype=np.float64)  # in [dB]
    samplefrequency = config.loc[1:, "Samplefrequency"].to_numpy(dtype=np.int32)  # in [Hz]

    # implement the usage of the vallen values for specific values

    # Ergebnisse: adc_microV unabhängig von der Samplefrequency und den Samples, von den Filtergrenzen
    #             adc_te unabhängig von der Anzahl der Samples, von den Filtergrenzen (umgekehrt proportional zur Samplefrequency, evtl. immer auf die gleiche Stelle runden)

    # following calculation of the range_factor does not match exactly the range_factor by vallen
    # 2.2 -> range in Volt with 10 percent buffer in both directions
    # 1e6 Volt to micro Volt
    # denominator: number of possible values in the numpy int16 space

    # variables_dict[
    #     "adc_microV_ch1"
    # ] = 1.56249975585941  # TODO replace with get_adc_microV #168.33334210069487824
    # variables_dict["adc_te_ch1"] = 0.000244140548706073  # 28.336114062789592438
    # variables_dict["adc_ss_ch1"] = 0.00156249975585941  # 1.6833334210069494929
    # variables_dict["adc_microV_ch2"] = 1.56249975585941  # 168.33334210069487824
    # variables_dict["adc_te_ch2"] = 0.000244140548706073  # 28.336114062789592438
    # variables_dict["adc_ss_ch2"] = 0.00156249975585941  # 1.6833334210069494929

    range_factor = (2.2 * range_V * 1e6) / (np.iinfo(np.int16).max - np.iinfo(np.int16).min)
    gain_factor = 10 ** (gain / 20)  # gain in [dB]
    adc_microV = range_factor / gain_factor
    adc_te = (1 / samplefrequency) * (range_factor / gain_factor) ** 2 * 100
    adc_ss = (
        adc_microV * 1000
    ) / samplefrequency  # adc_microV and samplefrequency arrays (entry1/entry1, entry2/entry2)
    ae_params = pd.DataFrame(
        {
            "ID": np.arange(1, adc_microV.size + 2),
            "SetupID": np.ones(adc_microV.size + 1, dtype=np.int8),
            "Chan": np.arange(0, adc_microV.size + 1),
            "ADC_µV": np.concatenate((np.array([0]), adc_microV)),
            "ADC_TE": np.concatenate((np.array([0]), adc_te)),
            "ADC_SS": np.concatenate((np.array([0]), adc_ss)),
        }
    )
    ae_params.index = np.arange(1, len(ae_params) + 1)

    return ae_params


def get_tr_params(config: pd.DataFrame) -> pd.DataFrame:
    """Determines the tr parameters from the measurement configuration

    Args:
        config (pd.DataFrame): acquisition configuration, see for details read or store acq_settings

    Returns:
        pd.DataFrame:  tr_params (ADC_microV and TR_mV)
    """
    # [x] important TODO implement this function get tr_params from config
    # [ ] INFO this function is fine, the rounding errors origin from get_ae_params

    LOGGER.info("Get_tr_params is not finally implemented. There maybe errors (2 digit after the dezimal point).")
    tr_params = get_ae_params(config)

    tr_params.drop(columns=["ADC_TE", "ADC_SS"], inplace=True)
    tr_mV = tr_params.loc[2:, "ADC_µV"].to_numpy(dtype=np.float64) / 1000
    tr_params["TR_mV"] = np.concatenate((np.array([0]), tr_mV))

    # tr_params = {}  # TODO limited to two channels (sufficient for the conditionWave)
    # tr_params[
    #     "adc_microV_ch1"
    # ] = 1.56249975585941  # 168.33334210069487824  # TODO replace with get_adc_microV
    # tr_params["tr_mV_ch1"] = 0.00156249975585941  # 0.16833334210069490488
    # tr_params["adc_microV_ch2"] = 1.56249975585941  # 168.33334210069487824
    # tr_params["tr_mV_ch2"] = 0.00156249975585941  # 0.16833334210069490488

    return tr_params


# Beispiel Fyrsonic mit 50µV Input-Range > 16 Bit Signed Integer
# 2^16 mapping -50µV bis + 50µV

# DATETIME_FORMAT_FILENAME = "%Y-%m-%d_%H-%M-%S"


##def _generate_filename(result: TestResult):
##    date = result.timestamp
##    date_str = date.strftime(DATETIME_FORMAT_FILENAME)
##    return f"{date_str}_{result.batch_number}_{result.serial_number}_ch{result.channel}"
##
##
##def _parse_filename(filename: str):
##    parts = filename.split("_")
##    datetime_str = "_".join((parts[0], parts[1]))
##    return dict(
##        datetime=datetime.strptime(datetime_str, DATETIME_FORMAT_FILENAME),
##        batch_number=parts[2],
##        serial_number=parts[3],
##        channel=parts[4][-1],
##    )


def datetime_str(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S.%f")


def generate_guid() -> str:
    return f"{{{str(uuid.uuid4()).upper()}}}"


def hit_from_tra(tra: vae.io.TraRecord) -> vae.io.HitRecord:
    """Generates a HitRecord from a TraRecord
    With the data of the transient record the acoustic emission features for the hit record are calculated

    Args:
        tra (vae.io.TraRecord): transient data record

    Returns:
        vae.io.HitRecord: acoustic emission features
    """
    # [ ] Review: ok to use the vae functions to determine the ae features?
    # [ ] TODO: literature check for the cascade values (cascade_hits, cascade_counts, cascade_energy, cascade_signal_strength)
    time = tra.time
    channel = tra.channel
    param_id = tra.param_id
    amplitude = vae.features.peak_amplitude(tra.data)
    duration = len(tra.data) / tra.samplerate  # not meaning full if measuring continuosly, in seconds
    energy = vae.features.energy(tra.data, tra.samplerate)
    rms = vae.features.rms(tra.data)
    signal_strength = vae.features.signal_strength(tra.data, tra.samplerate)  # Signal strength in nVs (1e-9 Vs)
    trai = tra.trai
    if tra.threshold > 0.0:
        hit = vae.io.HitRecord(
            time=time,
            channel=channel,
            param_id=param_id,
            amplitude=amplitude,
            duration=duration,
            energy=energy,
            rms=rms,
            threshold=tra.threshold,
            rise_time=vae.features.rise_time(tra.data, tra.threshold, tra.samplerate),
            signal_strength=signal_strength,
            counts=vae.features.counts(tra.data, tra.threshold),
            trai=trai,
        )
    else:
        hit = vae.io.HitRecord(
            time=time,
            channel=channel,
            param_id=param_id,
            amplitude=amplitude,
            duration=duration,
            energy=energy,
            rms=rms,
            rise_time=vae.features.rise_time(tra.data, tra.threshold, tra.samplerate, 0),
            signal_strength=signal_strength,
            trai=trai,
        )
    return hit


def connect_db(mode: str = "ro", compression: bool = True) -> Callable:
    # [ ] TODO remove the parameter compression and just use the compression defined in TraRecord?
    # waiting for update from Lukas
    def connect_db_outer(func: Callable) -> Callable:
        @wraps(func)
        def connect_db_inner(
            self: "DatabaseFile", *args: tuple, **kwargs: dict
        ) -> Any:  # [ ] Hack type annotation, how to annotate type (pridbfile, tradbfile, trfdbfile) without cycle import?
            """self is one of the DatabaseFiles (pridbfile, tradbfile, trfdbfile)

            Returns:
                Any:
            """
            try:
                # if not connected, first connect to abstract database and try to execute the abstract function
                # if the function is not implemented in the abstract database try to connect to the specific vae database
                #
                # compression is only in the init of the tradb-connection used -> after connecting the compression info is
                # stored as a class attribut _data_format
                if not (
                    self.db.connected == True
                ):  # not self.db.connect only does't work, because after the init connected is not set( not True nor False)
                    self.db = vae.io._database.Database(str(self.path), mode=mode, table_prefix=self.table_prefix)
                    LOGGER.info("Connected to abstract database")
                result = func(self, *args, **kwargs)
            except (
                AttributeError,
                NotImplementedError,
            ):  # caused, when the abstract database classs
                # has func not implemented (child class specific)
                if self.table_prefix == "tr":
                    # [ ] TODO check the compression parameter (how to pass it?)
                    if "compression" in kwargs:
                        self.db = vae.io.TraDatabase(
                            str(self.path),
                            mode=mode,
                            compression=kwargs["compression"],
                        )
                        kwargs.pop(
                            "compression"
                        )  # delete the kwarg compression, because it is only used for connecting
                        # to the tradb, but not for the function to execute!
                    else:  # [ ] TODO is compression as variable (not in the kwargs)
                        # possible? implementation before?
                        self.db = vae.io.TraDatabase(str(self.path), mode=mode, compression=True)

                    LOGGER.info("Connected to tradb")
                elif self.table_prefix == "trf":
                    self.db = vae.io.TrfDatabase(
                        str(self.path),
                        mode=mode,
                    )
                    LOGGER.info("Connected to trfdb")
                elif self.table_prefix == "ae":
                    self.db = vae.io.PriDatabase(
                        str(self.path),
                        mode=mode,
                    )
                    LOGGER.info("Connected to pridb")
                else:
                    logging.error("Database type not found. Maybe not implemented?")
                    raise
                result = func(self, *args, **kwargs)
            except OperationalError:
                logging.exception(msg="sqlite3 error.", exc_info=True)
                raise
            self.db.close()

            return result

        return connect_db_inner

    return connect_db_outer


def read_acq_settings(db_path: PurePath) -> pd.DataFrame:
    """read the acquisition settings
    The numeric values are casted to floats. This is currently the only option to handle also None values. (As floats nans)
    Args:
        db_path (PurePath): path to the database

    Returns:
        pd.DataFrame: acquisition settings
    """
    engine = sa.create_engine(f"sqlite:///{db_path}")
    insp = sa.inspect(engine)
    tables = list(insp.get_table_names())
    # the table exists only in databases created later than the 28.10.2021, or in updated ones!
    if "acq_settings" in tables:
        acq_settings = pd.read_sql_table("acq_settings", engine)
        if not acq_settings.empty:
            # following check is needed, to support old acq_settings versions (used from 11/2021 to 20/12/2021)
            if "index" in acq_settings.columns:
                if not isinstance(acq_settings.index.dtype, int):
                    acq_settings.index = acq_settings.index.astype(int)
                    acq_settings = acq_settings.sort_index()

            elif "Key" in acq_settings.columns:
                # [ ] Review maybe drop this, and modify all files
                # old acq_settings versions (used from 11/2021 to 20/12/2021)
                acq_settings = acq_settings.set_index("Key")
                acq_settings = acq_settings.transpose()
                acq_settings = acq_settings.reset_index(drop=True)
                acq_settings.index = acq_settings.index.rename("index")
                acq_settings.loc[1:, "Channel Description"] = acq_settings.loc[1:, "Channel"]
                acq_settings.loc[1:, "Channel"] = acq_settings.index[
                    1:
                ]  # not always true, but for the fyrsonic measurements to convert it is true
                columns = [
                    "Device",
                    "All channels same config",
                    "Channel",
                    "Channel Description",
                    "Measurement mode",
                    "Range",
                    "Preamplifier gain",
                    "Samplefrequency",
                    "Highpass Filter Cutoff Frequency",
                    "Lowpass Filter Cutoff Frequency",
                    "Filterorder",
                    "Blocksize",
                    "Additional Text",
                ]
                for col in columns:
                    if col not in acq_settings.columns:
                        acq_settings[col] = None
                if acq_settings.loc[0, "Range"] == "[mV]":
                    acq_settings.loc[1:, "Range"] = 1e-3 * acq_settings.loc[1:, "Range"].astype(int)
                acq_settings = acq_settings[columns]  # reorder the columns
                acq_settings.iloc[0] = [
                    "[-]",
                    "[-]",
                    "[-]",
                    "[-]",
                    "[-]",
                    "[V]",
                    "[dB]",
                    "[Hz]",
                    "[Hz]",
                    "[Hz]",
                    "[-]",
                    "[-]",
                    "[-]",
                ]
            else:
                LOGGER.warning("Not support version of the acq_settings in the database.")

        # old style before 24.11.2021
        # LOGGER.debug("Old style acq_settings table. Used before 24.11.2021")
        # acq_settings = df.set_index("Key").T.to_dict("list")
        # acq_settings["Range"][0] = int(acq_settings["Range"][0])
        # acq_settings["Preamplifier gain"][0] = int(acq_settings["Preamplifier gain"][0])
        # acq_settings["Samplefrequency"][0] = int(acq_settings["Samplefrequency"][0])
        # acq_settings["Highpass Filter Cutoff Frequency"][0] = (
        #     int(acq_settings["Highpass Filter Cutoff Frequency"][0])
        #     if acq_settings["Highpass Filter Cutoff Frequency"][0]
        #     else None
        # )
        # acq_settings["Lowpass Filter Cutoff Frequency"][0] = (
        #     int(acq_settings["Lowpass Filter Cutoff Frequency"][0])
        #     if acq_settings["Lowpass Filter Cutoff Frequency"][0]
        #     else None
        # )
        # acq_settings["Blocksize"][0] = int(acq_settings["Blocksize"][0])

    else:
        LOGGER.warning("Could not read the acquisition configuration!")
        LOGGER.warning("This is mostly the case for dbs created before October 2021.")
        acq_settings = pd.DataFrame()
    # [ ] TODO @KB replace that for loop
    # [ ] Review mixed datatype problematic in pandas DataFrame? first line everything string, other lines, floats
    for col, values in acq_settings.iteritems():
        acq_settings[col] = values.replace("None", np.nan)
        acq_settings[col] = values.replace("False", False)
        acq_settings[col] = values.replace("True", True)
    # casted to floats to work with the None entries
    acq_settings.loc[1:, "Range":"Blocksize"] = acq_settings.loc[1:, "Range":"Blocksize"].astype(float)
    acq_settings.loc[1:, "Channel"] = acq_settings.loc[1:, "Channel"].astype(int)
    return acq_settings


def store_acq_settings(
    dbfile_path: PurePath, acq_settings: pd.DataFrame
) -> None:  # [ ] Update: Candidate for abstract filehandler of all vallen databases
    # [ ] TODO update this doc string
    """Stores the acquisition settings of the measurement in the database
    All entries in the DataFrame are casted to strings
    Args:
        dbfile_path (PurePath): db to store the acq_settings
        acq_settings (pd.DataFrame):Key - Unit - Channel 1 - Channel 2 - furthermore channels
            Channel [-], str, channel description
            Measurement mode [-], Steaming, Hit based
            Range [mV], int, 10
            Preamplifier gain [dB], int, 0
            Samplefrequency [Hz], int, 100000
            Highpass Filter Cutoff Frequency [Hz], Optional(int), 1500
            Lowpass Filter Cutoff Frequency [Hz], Optional(int), None
            Blocksize [-], int , 1024
            Additional Text [-], str, Additional Infos, like general Messsetup,
                Temperature, specific data of the measurement
            Channel: Sensor description (Type, Serialnumber, Orientation, Location, ...)
    """
    # [x] TODO currently only working for two channels (Fyrsonic) -> make it work for abitrary number of channels
    engine = sa.create_engine(f"sqlite:///{dbfile_path}")
    insp = sa.inspect(engine)

    if insp.has_table("acq_settings"):
        LOGGER.warning("acq_settings already in the database.")
        LOGGER.warning("Going to update the settings.")
        old_acq_settings = pd.read_sql_table("acq_settings", engine)
        LOGGER.info("Here are the old settings:")
        print(old_acq_settings)
    acq_settings = acq_settings.astype(str)
    acq_settings.to_sql(
        name="acq_settings",
        con=engine,
        if_exists="replace",
        index=True,
        dtype=sa.types.Text,
    )
    # sqlite3_code_path = PurePath(SQLITE3CODE_PATH, "insert_acq_settings.sql")0
    # sqlite3code = SQLite3Code(file_obj=sqlite3_code_path)
    # data = acq_settings.loc[:, "Channel 1"]
    # data["ch"] = "Channel 1"
    # sqlite3code.assign_variables(data)
    # sqlite3code.executeScript(dbfile.db.connection())

    # acq_settings.drop(columns=["Channel 1", "Unit"])
    # for ch, data in acq_settings.iteritems():
    #     data = data.to_dict()
    #     data["ch"] = ch
    #     sqlite3_code_path = PurePath(SQLITE3CODE_PATH, "acq_settings_add_channel.sql")
    #     sqlite3code = SQLite3Code(file_obj=sqlite3_code_path)
    #     sqlite3code.assign_variables(data)
    #     sqlite3code.executeScript(dbfile.db.connection())


def set_timebase(db: Vaedatabase, timebase: int) -> None:
    """updates the default timebase (1e7) from the creation of the database

    Args:
        db (vae.io.PriDatabase or vae.io.TraDatabase): db to update the timebase
        timebase (int): new value for the timebase
    """
    db._timebase = timebase  # very import to update the _timebase in the PriDatabase
    # (Python object)
    if type(db) == PriDatabase:
        sqlite3_code_path = PurePath(SQLITE3CODE_PATH, "update_timebase_pridb.sql")
    else:
        sqlite3_code_path = PurePath(SQLITE3CODE_PATH, "update_timebase_tradb.sql")
    sqlite3code = SQLite3Code(file_obj=sqlite3_code_path)
    variables_dict = {"timebase": timebase}
    sqlite3code.assign_variables(variables_dict)
    sqlite3code.executeScript(db.connection())


def set_filestatus(db: Vaedatabase, filestatus: int) -> None:
    """update the file status in the database

    Args:
        db (vae.io.PriDatabase, vae.io.TraDatabase, vae.io.TrfDatabase): db to update the filestatus
        filestatus (int): new status (0: offline, 1: suspended, 2: active)
    """
    # [ ] Review when to use which status

    sqlite3_code_path = PurePath(SQLITE3CODE_PATH, "set_filestatus.sql")
    sqlite3code = SQLite3Code(file_obj=sqlite3_code_path)

    if db._table_prefix == "ae":
        table_prefix = "ae"
    elif db._table_prefix == "tr":
        table_prefix = "tr"
    elif db._table_prefix == "trf":
        table_prefix = "trf"
    else:
        LOGGER.warning(f"Unknown table prefix: {db._table_prefix}")
    variables_dict = {"table": table_prefix, "filestatus": filestatus}
    sqlite3code.assign_variables(variables_dict)
    sqlite3code.executeScript(db.connection())


def write_guid(
    dbfile: "DatabaseFile",
) -> None:  # [ ] Update: Candidate for abstract filehandler of all vallen databases
    """Writes a generated guuid in the Database"""
    guid = generate_guid()
    script = f"UPDATE {dbfile.table_prefix}_globalinfo SET Value = '{guid}' WHERE Key == 'FileID';"
    dbfile.db.connection().executescript((script))


@connect_db(mode="ro")
def read_global_info(dbfile: "DatabaseFile") -> pd.DataFrame:
    """read the global info of the Vallen Database File

    Returns:
        pd.DataFrame: global info
    """
    data = dbfile.db.globalinfo()

    return data


@connect_db(mode="ro")
def get_first_last_trai(dbfile: "DatabaseFile") -> Tuple[int, int]:
    """Reads the first and the last trai in the Vallen Database

    Returns:
        Tuple[int, int]: first trai, last trai
    """
    trai_start = dbfile.db.connection().execute(f"SELECT min(TRAI) FROM {dbfile.table_prefix}_data;").fetchone()
    if trai_start is None:
        trai_start = 0
    elif isinstance(trai_start, Tuple):
        trai_start = min(trai_start)
    trai_stop = dbfile.db.connection().execute(f"SELECT max(TRAI) FROM {dbfile.table_prefix}_data;").fetchone()
    if trai_stop is None:
        trai_stop = 0
    elif isinstance(trai_stop, Tuple):
        trai_stop = max(trai_stop)

    return trai_start, trai_stop


def pridb_from_tradb(
    tradbfile_path: PurePath,
    tradb_data: Optional[pd.DataFrame] = None,
    name_extension: Optional[str] = None,
) -> PurePath:
    """Creates a pridb with the data from the tradb
    with the same name (.pridb) at the same folder

    Args:
        tradbfile_path (PurePath): Path to the Tradbfile with the transient data
        tradb_data: Optional[pd.DataFrame]: option to pass the tradb-data directly, bad performance, but needed for change the raw data
            -> better performance: save another tradb with the modified data and than call this function and read the data from file,
            defaults to None
        name_extension: Optional[str]:  add that string to the original filename (of the tradbfile_path),
            defaults to None

    Returns:
        PurePath:   Path to the new pridb
    """
    # [ ] TODO @AH einfacheren Weg, kann ich nicht den ganzen tradbfile_path als filename übergeben, oder als fullpath?
    wkd = tradbfile_path.parent
    filename = tradbfile_path.name
    f = FileHandler(filename=filename, wkd=wkd)
    tradb_file = f.current_file
    if name_extension:
        pridb_name = f"{tradb_file.shortname}{name_extension}.pridb"
    else:
        pridb_name = f"{tradb_file.shortname}.pridb"
    f.set_file(pridb_name)
    pridb_file = f.current_file
    config = read_acq_settings(
        tradb_file.path
    )  # [ ] TODO @KB only working if the acq_settings are stored in the tradb (not before 28.10.2021)
    if tradb_data:
        for ch in range(1, len(tradb_data.channel.unique()) + 1):
            config.loc[ch, "Samplefrequency"] = tradb_data[tradb_data.channel == ch].samplerate.unique()[0]
            # [ ] TODO don't forget, the possibility that the acquisition configs for different channels can be different!
            # config["Highpass Filter Cutoff Frequency"] # [ ] TODO update these values if filtering is possible
            # config["Lowpass Filter Cutoff Frequency"] # [ ] TODO update these values if filtering is possible
            config.loc[ch, "Blocksize"] = tradb_data[tradb_data.channel == ch].samples.unique()[0]
    with pridb_file(mode="rwc") as pridb:
        pridb.create(config)
        LOGGER.info(f"Created empty pridb: {pridb.name}")
        if isinstance(tradb_data, pd.DataFrame):
            today = datetime.now()
            LOGGER.info("Measurement start is not given. Using current time stamp!")
            pridb.write_start_markers(today)
            try:
                for trai, tra in tradb_data.iterrows():
                    tr_record = TraRecord(**tra, trai=trai)
                    hit = hit_from_tra(tr_record)
                    pridb.write(hit, tr_record.samplerate, tr_record.samples)
            except Exception as e:
                LOGGER.error("Error during writing hits from tras: %s", e)
            last_time_point = tradb_data.iloc[-1].time
        else:
            with tradb_file() as tradb:
                # [ ] TODO read other needed info from tradb to copy in the pridb
                measurement_start = tradb.get_measurement_start_timepoint()
                pridb.write_start_markers(
                    measurement_start,
                )
                iterable = tradb.db.iread()
                try:
                    for tra in iterable:
                        # tra is a TraRecord!
                        hit = hit_from_tra(tra)
                        pridb.write(hit, tra.samplerate, tra.samples)
                        last_time_point = tra.time
                except Exception as e:
                    LOGGER.error("Error during writing hits from tras: %s", e)

                # last_time_point = tradb.get_measurement_duration()

        con = pridb.db.connection()
        cur = con.execute("SELECT Time FROM view_ae_data ORDER BY SetID DESC LIMIT 1")
        try:
            timemax = cur.fetchone()[0]  # None is not subscriptable -> TypeError
        except TypeError:
            timemax = 0
        if last_time_point + 1e-9 > timemax:
            pridb.insert_marker(
                time=last_time_point,
                set_type=4,
                data="Stop recording",
                number=2,
            )
        else:
            pridb.insert_marker(
                time=timemax + 2e-9,
                set_type=4,
                data="Stop recording",
                number=2,
            )
        pridb.set_all_sets_valid()
    return pridb_file.path


def pridb_live_generation(tradbfile_path: PurePath, trai_start: Optional[int] = None) -> None:
    """Live generation of a pridb with the data from the tradb, during writing measurement data in the tradb
    The pridb has the same name and directory as the tradb
    The pridb has to be created before this function is called

    Args:
        tradbfile_path (PurePath): Path to the Tradbfile with the transient data
        trai_start(int):    first TRAI to read, needed if the tradb and pridb is used for previous measurements

    Returns:
        Tuple(float, int):  last written timepoint, last TRAI
    """
    wkd = tradbfile_path.parent
    filename = tradbfile_path.name
    f = FileHandler(filename=filename, wkd=wkd)
    if not f.exist_file():
        sleep(1.5)
    if not f.exist_file():
        raise FileNotFoundError("Tradb file does not exist!")
    tradb_file = f.current_file
    f.set_file(f"{tradb_file.shortname}.pridb")
    pridb_file = f.current_file
    if trai_start:
        query_filter = f"TRAI >= {trai_start}"
    else:
        query_filter = None
    with tradb_file(mode="ro") as tradb, pridb_file(mode="rw") as pridb:
        tradb_data = tradb.db.listen(existing=True, query_filter=query_filter)  # getting a generator
        for tra in tradb_data:
            hit = hit_from_tra(tra)
            pridb.write(hit, tra.samplerate, tra.samples)
        pridb.write_stop_marker(tra.samplerate)


def trfdb_live_generation(
    tradbfile_path: PurePath,
    trai_start: Optional[int] = None,
    feature_selection: Optional[List[str]] = ["All"],
) -> None:
    """Live generation of a trfdb with the data from the tradb, during writing measurement data in the tradb
    The trfdb has the same name and directory as the tradb
    The trfdb has to be created before this function is called

    Args:
        tradbfile_path (PurePath): Path to the Tradbfile with the transient data
        trai_start(int):    first TRAI to read, needed if the tradb and pridb is used for previous measurements

    Returns:
        Tuple(float, int):  last written timepoint, last TRAI
    """
    wkd = tradbfile_path.parent
    filename = tradbfile_path.name
    f = FileHandler(filename=filename, wkd=wkd)
    if not f.exist_file():
        sleep(1.5)
    if not f.exist_file():
        raise FileNotFoundError("Tradb file does not exist!")
    tradb_file = f.current_file
    f.set_file(f"{tradb_file.shortname}.trfdb")
    trfdb_file = f.current_file
    if trai_start:
        query_filter = f"TRAI >= {trai_start}"
    else:
        query_filter = None
    with tradb_file(mode="ro") as tradb, trfdb_file(mode="rw") as trfdb:
        tradb_data = tradb.db.listen(existing=True, query_filter=query_filter)  # getting a generator
        # following for loop has to be in the with-statement, otherwise an error is
        # raised because the database connection is closed
        for tra in tradb_data:
            features = feature_calculation(
                tra.data,
                tra.channel,
                tra.trai,
                tra.time,
                tra.samplerate,
                tra.pretrigger,
                feature_selection=feature_selection,
            )
            trfdb.write(features)
        tradb.db.close()


def trfdb_from_tradb(
    tradbfile_path: PurePath,
    tradb_data: Optional[pd.DataFrame] = None,
    name_extension: Optional[str] = None,
    feature_selection: Optional[List] = ["All"],
) -> PurePath:
    """Creates a trfdb with the data from the tradb
    with the same name (.trfdb) at the same folder

    Args:
        tradbfile_path (PurePath): Path to the Tradbfile with the transient data
        tradb_data: Optional[pd.DataFrame]: option to pass the tradb-data directly, bad performance, but needed for change the raw data
            -> better performance: save another tradb with the modified data and than call this function and read the data from file,
            defaults to None
        name_extension: Optional[str]:  add that string to the original filename (of the tradbfile_path),
            defaults to None
        feature_selection: Optional[List]: select the features to calculate,
            defaults to "All"

    Returns:
        PurePath: path of the new trfdb
    """
    # [ ] TODO: add possibility to change the blocksize
    # [ ] TODO: add possibility to filter the transient data
    # [ ] TODO: add possibility to use a window before calculating the fft
    # [ ] TODO @AH einfacheren Weg, kann ich nicht den ganzen tradbfile_path als filename übergeben, oder als fullpath?
    wkd = tradbfile_path.parent
    filename = tradbfile_path.name
    f = FileHandler(filename=filename, wkd=wkd)
    tradb_file = f.current_file
    if name_extension:
        trf_name = f"{tradb_file.shortname}{name_extension}.trfdb"
    else:
        trf_name = f"{tradb_file.shortname}.trfdb"

    f.set_file(trf_name)
    trfdb_file = f.current_file
    config = read_acq_settings(
        tradbfile_path
    )  # [ ] TODO @KB only working if the acq_settings are stored in the tradb (not before 28.10.2021)
    if tradb_data:
        for ch in range(1, len(tradb_data.channel.unique()) + 1):
            config.loc[ch, "Samplefrequency"] = tradb_data[tradb_data.channel == ch].samplerate.unique()[0]
            # [ ] TODO don't forget, the possibility that the acquisition configs for different channels can be different!
            # config["Highpass Filter Cutoff Frequency"] # [ ] TODO update these values if filtering is possible
            # config["Lowpass Filter Cutoff Frequency"] # [ ] TODO update these values if filtering is possible
            config.loc[ch, "Blocksize"] = tradb_data[tradb_data.channel == ch].samples.unique()[0]

    with trfdb_file(mode="rwc") as trfdb:
        trfdb.create(config)
        LOGGER.info(f"Created empty trfdb: {trfdb.name}")
        if isinstance(tradb_data, pd.DataFrame):
            try:
                for trai, tra in tradb_data.iterrows():
                    features = feature_calculation(
                        tra.data,
                        tra.channel,
                        trai,
                        tra.time,
                        tra.samplerate,
                        tra.pretrigger,
                        feature_selection=feature_selection,
                    )
                    trfdb.write(features)
            except Exception as e:
                LOGGER.error("Error during writing features from tras: %s", e)
        else:
            with tradb_file() as tradb:
                # [ ] TODO read other needed info from tradb to copy in the pridb
                iterable = tradb.db.iread()
                try:
                    for tra in iterable:
                        features = feature_calculation(
                            tra.data,
                            tra.channel,
                            tra.trai,
                            tra.time,
                            tra.samplerate,
                            tra.pretrigger,
                            feature_selection=feature_selection,
                        )
                        trfdb.write(features)
                except Exception as e:
                    LOGGER.error("Error during writing features from tras: %s", e)
    return trfdb_file.path


# [ ] Review: class method of TradbFile and work with object data, or utils method to reshape data from outside also?
def get_new_blocksize(tr_data: pd.DataFrame, blocksize: int, fit_size: str = "crop") -> pd.DataFrame:
    """Splits the transient (tr_) data in blocks with the new blocksize

    Currently the measurement parameters for every channel should be the same!
    The first Trai entry keeps the same -> becarefull, when mixing different measurements with new blocksize:
    Maybe there are discontinuties or duplicates in the trais

    Args:
        tr_data (pd.DataFrame): transient data to reshape
        blocksize (int): new blocksize, use only power of 2, e.g.: ..., 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, ..
            -> better performance, if calculating the fft afterwards
        fit_size (str): crop: crop the data after the last complete block
                        zeropad: zero-pad the data

    Returns:
        pd.DataFrame: data splitted in new blocksize
    """
    # [x] TODO implement reshape on the pandas dataframe
    # [ ] TODO implement the corresponding test!
    # [ ] TODO only working for trai ranges with the same measurement parameters (pretrigger, threshold, samplerate)
    # logging.exception("Not yet implemented")
    # [ ] TODO implement saving of the new tradb!
    df_l = []
    for ch, entries in tr_data.groupby("channel"):
        channel_data = np.hstack(entries["data"])
        modulo_value = channel_data.size % blocksize
        if modulo_value != 0:
            if fit_size == "crop":
                channel_data = channel_data[:-modulo_value]
            elif fit_size == "zeropad":
                pad_width = blocksize - modulo_value
                channel_data = np.pad(channel_data, (0, pad_width), "constant")
            else:
                LOGGER.warning(
                    "The size of the data don't fit in the new blocksize and no valid option for fitting the size is given."
                )
                LOGGER.info("Crop and zeropad are valid options.")
        channel_data = channel_data.reshape((-1, blocksize))
        time_step_old = entries["samples"].unique()[0] / entries["samplerate"].iloc[0]
        time_step_new = blocksize / entries["samplerate"].iloc[0]
        t_start = entries["time"].iloc[0] - time_step_old
        time = t_start + time_step_new + np.arange(0, channel_data.shape[0]) * time_step_new
        df = pd.DataFrame(time, columns=["time"])
        df["channel"] = ch
        df["param_id"] = entries["param_id"].iloc[0]
        df["pretrigger"] = entries["pretrigger"].iloc[0]
        df["threshold"] = entries["threshold"].iloc[0]
        df["samplerate"] = entries["samplerate"].iloc[0]
        df["samples"] = blocksize
        df["data"] = channel_data.tolist()  # [ ] TODO @AH is there another way than using that tolist?
        df_l.append(df)
        data = pd.concat(df_l, ignore_index=True, sort=False)
        data.sort_values(by="time", axis=0, inplace=True)
        data.reset_index(drop=True, inplace=True)
        data.index = data.index + 1
        data.index.names = ["trai"]
    return data


# [ ] TODO: add a function to filter the data (similiar to the filter during the acquisition!)


def modify_raw_data_for_features(
    tr_data: pd.DataFrame,
    blocksize: int,
    fit_size: Optional[str] = "crop",
    feature_selection: Optional[List] = ["All"],
    save: Optional[bool] = False,
    tradbfile_path: Optional[PurePath] = None,
    name_extension: Optional[str] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Modifies the transient data (raw data) and calculates the new acoustic emission and other features

    Args:
        tr_data (pd.DataFrame): original transient data of the measurement
        blocksize (int): new blocksize, use only power of 2, e.g.: ..., 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, ..
            -> better performance, if calculating the fft afterwards
        fit_size (str): crop: crop the data after the last complete block
                        zeropad: zero-pad the data, Defaults to crop
        feature_selection Optional[List]:   select the features to calculate, Defaults to ["All"]
        save Optional[bool]:    save the new data in pridb, trfdbs or not,
            if saving is chosen, the returnd hits and features DataFrames are empty!
            defaults to False
        tradbfile_path Optional[PurePath]:  path to the original tradbfile, directory of the new files and needed for the filenames,
            if no path is given the data is not saved!,
            defaults to None
        name_extension Optional[str]:   extension to the original filename, following extension is automatically made: "_Blocksize_{blocksize}",
            defaults to None

    Returns:
        (pd.DataFrame): new transient data
        (pd.DataFrame): new acoustic emission data (pridb data)
        (pd.DataFrame): new features
    """
    # [ ] TODO: current implementation all transient data loaded and new feature data is calculated -> maybe option to work with the database files
    tr_new = get_new_blocksize(tr_data, blocksize, fit_size)

    # [ ] TODO: implement filter data
    # [ ] TODO: implement resampling
    if save and tradbfile_path:
        if name_extension:
            name_extension = f"_Blocksize_{blocksize}_{name_extension}"
        else:
            name_extension = f"_Blocksize_{blocksize}"
        LOGGER.info("Going to save the new features in a pridb and a trfdb.")
        LOGGER.info(f"The names of the files are: {tradbfile_path.stem}{name_extension}")
        pridb_fullpath = pridb_from_tradb(tradbfile_path, tr_new, name_extension)
        trfdb_fullpath = trfdb_from_tradb(tradbfile_path, tr_new, name_extension, feature_selection)
        f = FileHandler(filename=pridb_fullpath.name, wkd=pridb_fullpath.parent)
        with f.current_file(mode="ro") as pridb:
            hits = pridb.read()
        f.set_file(trfdb_fullpath.name)
        with f.current_file(mode="ro") as trfdb:
            features = trfdb.read()
    else:
        hit_l = []
        features_l = []
        # [ ] TODO optimize following for loop (vectorize the computations)
        for trai, data in tr_new.iterrows():
            tr_record = TraRecord(**data, trai=trai)
            hit = hit_from_tra(tr_record)
            hit_l.append(hit)
            features = feature_calculation(
                tr_record.data,
                tr_record.channel,
                tr_record.trai,
                tr_record.time,
                tr_record.samplerate,
                tr_record.pretrigger,
                feature_selection=feature_selection,
            )
            features_l.append(features)

        hits = pd.DataFrame(hit_l)
        features = pd.DataFrame(features_l)

    return tr_new, hits, features


def match_time_to_trai(
    time_abs: pd.Timestamp,
    meas_start_abs: pd.Timestamp,
    blockduration: float,
    trai_start: int,
    channels: int,
) -> Tuple[int]:
    """[summary]

    Args:
        time_abs (datetime): [description]
        meas_start_abs (datetime): [description]
        blockduration (float): duration of one block in seconds
        trai_start (int): first trai
        channels (int): number of channels

    Returns:
        Tuple[int]: corresponding trais of all channels

    Check your data carefully. The altering pattern of th channels may change!
    And check that for all timepoints measurement data of all channels are recorded!
    """
    # [ ] TODO error bone, at the start and the end there may not measurement samples for all channels!!
    # [ ] TODO bei Bedarf auch noch zu der  Numer des Samples in dem jeweiligen Block matchen!
    # [ ] Review die Zuordnung zu dem jeweiligen Sample ist wahrscheinlich nicht sinnvoll, wegen Benutzerverzögerung
    #  und einer geringeren Abtastfrequenz der Metadaten! -> nur Zuordnung zu den Blöcken
    # [ ] TODO Assumption that the channels alter on a regular basis -> not always true!
    time_delta = (time_abs - meas_start_abs).total_seconds()
    if time_delta < 0.0:
        LOGGER.info("Timestamp before measurement start. Setting TRAI to first TRAI value.")
        LOGGER.info("Ok, for meta data.")
        trai = trai_start
    else:
        trai = int(time_delta // blockduration)
        trai = trai_start + channels * trai

    trais = tuple(range(trai, trai + channels))

    return trais
