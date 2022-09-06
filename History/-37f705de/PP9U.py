"""Read pridb files"""
import logging
from datetime import datetime
from pathlib import Path, PurePath
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
import sqlalchemy as sa
import vallenae as vae
from atoolbox import BaseFile, SQLite3Code
from vallenae.io.pridb import PriDatabase

from vallendb.vdbFileHandler.utils import (
    connect_db,
    datetime_str,
    get_ae_params,
    set_filestatus,
    set_timebase,
    store_acq_settings,
    write_guid,
)

LOGGER = logging.getLogger(__name__)
SQLITE3CODE_PATH = PurePath(Path(__file__).resolve().parent, "sqlite3_code")
TIMEFORMAT = "%Y-%m-%d %H:%M:%S.%f"


class PridbFile(BaseFile):
    """Special File Operations"""

    # [x] TODO Add context manager functionality: __enter__ and __exit__ method
    # [x] TODO Remove connection decorator

    def __init__(self, file_obj: PurePath):
        """Inherit all attributes and methods from the BaseFile Class

        Args:
            file_obj (PurePath): filename and location"""
        super().__init__(file_obj)
        self._check_filetypes((".pridb",))
        self.table_prefix = "ae"
        self.db = PriDatabase
        self.ae_params = dict()
        self.mode = str()
        self.channels = {}
        self.data = pd.DataFrame()
        # if not config:  # default config
        #     config = {
        #         "MeasurementMode": "Streaming",
        #         "Pretrigger": 0,
        #         "Range": "50 mV",
        #         "PreamplifierGain": "0 dB",
        #         "Samplefrequency": 10000000,
        #         "Filter-LowerLimit": None,
        #         "Filter-UpperLimit": None,
        #         "Filter-Order": 8,
        #         "Blocksize": 65536,
        #     }

    # call is needed to pass arguments to the enter function
    def __call__(self, mode: str = "ro"):
        """context manager function to pass arguments to the enter function

        Args:
            mode (str, optional): Mode of the database connection: "ro": read-only
                                    "rw": read-write
                                    "rwc": read-write-create
                                    Defaults to "ro".

        Returns:
            [type]: pass the class instance to the enter method
        """
        self.mode = mode
        return self

    def __enter__(
        self,
    ) -> vae.io.TraDatabase:
        """Connects to the database in an with-statement

        Returns:
            vae.io.TraDatabase: TraDatabase object of the specified tradb
        """
        # [ ] TODO add here or in create a warning if file alread exists, also in trfdb and tradb
        self.db = vae.io.PriDatabase(filename=self.path, mode=self.mode)
        if self.mode in [
            "rwc",
            "rw",
        ]:  # not possible to write file status if mode = "ro"
            filestatus = 2
            set_filestatus(self.db, filestatus)
        return self

    def __exit__(self, type, value, traceback) -> None:
        """Exit method to close the database at the end of the with statement

        Args:
            type ([type]): type of exceptions occured in the with-statement
            value ([type]): value of the exceptions
            traceback ([type]): traceback of the exceptions
        """
        if self.mode in [
            "rwc",
            "rw",
        ]:  # not possible to write file status if mode = "ro"
            set_filestatus(self.db, 0)
        self.db.close()

    def create(self, config: pd.DataFrame) -> None:
        """Create a vallenae primary database.

        Using the maximum samplefrequency of all channels as timebase

        Args:
            config (pd.DataFrame):  Columns acquisition configuration, first row units, following rows channel data"""

        set_timebase(self.db, config.loc[1:, "Samplefrequency"].astype(np.int32).max())
        write_guid(self)
        self.determine_write_ae_params(config)
        store_acq_settings(self.path, config)

    def read(
        self,
        **kwargs: dict,
    ) -> Dict[str, pd.DataFrame]:
        """Load a file.

        channel: None if all channels should be read.
                Otherwise specify the channel number or a list of channel numbers
        time_start: Start reading at relative time (in seconds). Start at beginning
            if `None`
        time_stop: Stop reading at relative time (in seconds). Read until end if `None`
        hit: Read data by Hit (transient recorder index)
        query_filter: Optional query filter provided as SQL clause,
                e.g. "Pretrigger == 500 AND Samples >= 1024"

        Returns: Dict[str, pd.DataFrame]: {"CH1": data of that channel, "CH2": data of that channel}

        """
        # [ ] TODO Handle measurement start and stop (there are multiple entries per channel for one time point!)
        data = self.db.read(**kwargs)
        data["Time rel. [s]"] = data["time"] - data["time"].iloc[0]
        # drop empty rows (start, stop of the measurement)
        data.dropna(thresh=9, inplace=True)
        self.data = data
        self.channels = {f"CH{name}": x for name, x in data.groupby("channel")}
        return self.data

    def read_markers(self, **kwargs: Dict[str, Any]) -> pd.DataFrame:
        """Read marker to Pandas DataFrame.

        Args:
            **kwargs: Arguments passed to `iread_markers`

        Returns:
            Pandas DataFrame with marker data
        """
        markers = self.db.read_markers(**kwargs)
        return markers

    def read_own_markers(self) -> pd.DataFrame:
        """reads the measurement markers
        Stored in the own table "Measurement Markers"

        Returns:
            pd.DataFrame: read and parsed markers
        """
        engine = sa.create_engine(f"sqlite:///{self.path}", echo=False)
        data = pd.read_sql_table(table_name="Measurement Markers", con=engine)
        data["Start TRAI"] = data["Start SetID"].map(self.setid_to_trai)
        data["Stop TRAI"] = data["Stop SetID"].map(self.setid_to_trai)
        data["Start rel. [s]"] = data["Start SetID"].map(self.setid_to_time)
        data["End rel. [s]"] = data["Stop SetID"].map(self.setid_to_time)
        data["Measurement duration [s]"] = (data["End abs."] - data["Start abs."]).dt.total_seconds()

        return data

    def parse_markers(self) -> pd.DataFrame:
        """Parses the markers

        Returns:
            pd.DataFrame: 'Start abs.': absolute timestamp of the measurement start
             'End abs.': absolute timestamp of the measurement end
             'Start rel.': relative timepoint of the measurement start
             'End rel.': relative timepoint of the measurement end
             'Measurement start SetID': setID of the measurement start
             'Measurement end SetID': setID of the measurement end
             'Measurement duration': duration of the measurements in seconds
        """
        # [ ] TODO trais of the measurements needed?
        # [ ] TODO check if the measurment duration of the abs. and the rel.

        # [x] TODO important check, ob die pridb nachträglich aus der tradb erzeugt wurde (checken ob es die Tabelle Measurement Markers gibt)
        # [ ] TODO add test for that check

        engine = sa.create_engine(f"sqlite:///{self.path}", echo=False)
        insp = sa.inspect(engine)
        tables = list(insp.get_table_names())
        # following check is important, than a pridb generated during the measurement has NULL-rows at the start/stops
        if "Measurement Markers" in tables:
            # the pridb is generated from the tradb afterwards
            df = self.read_own_markers()
        else:
            # time is equal
            markers = self.read_markers()
            startpoints_abstime = markers.data[1::5].tolist()
            endpoints_abstime = markers.data[3::5].tolist()
            startpoints_reltime = markers.time[0::5]
            endpoints_reltime = markers.time[3::5]
            measurement_setid_start = markers.index[2::5] + 1
            measurement_setid_end = markers.index[3::5] - 1
            start_trai = list(map(self.setid_to_trai, measurement_setid_start))
            end_trai = list(map(self.setid_to_trai, measurement_setid_end))
            columns = [
                "Start TRAI",
                "Stop TRAI",
                "Start abs.",
                "End abs.",
                "Start rel. [s]",
                "End rel. [s]",
                "Start SetID",
                "Stop SetID",
            ]
            df = pd.DataFrame(
                list(
                    zip(
                        start_trai,
                        end_trai,
                        startpoints_abstime,
                        endpoints_abstime,
                        startpoints_reltime,
                        endpoints_reltime,
                        measurement_setid_start,
                        measurement_setid_end,
                    )
                ),
                columns=columns,
            )
            df["Start abs."] = pd.to_datetime(df["Start abs."], format=TIMEFORMAT)
            df["End abs."] = pd.to_datetime(df["End abs."], format=TIMEFORMAT)
            df["Measurement duration rel. [s]"] = df["End rel. [s]"] - df["Start rel. [s]"]
            df["Measurement duration abs. [s]"] = (df["End abs."] - df["Start abs."]).dt.total_seconds()
            if not np.isclose(df["Measurement duration rel. [s]"], df["Measurement duration abs. [s]"]).all():
                # this warning is expected for all measurments for SmartSAD August 2021
                # (bug in the measurement interface)
                LOGGER.warning(
                    "The measurement duration determined from the abs. timestamps differs from the duration determined with the measurement data!"
                )
                df.rename(columns={"Measurement duration abs. [s]": "Measurement duration [s]"})
                df.drop(columns=["Measurement duration rel. [s]"], inplace=True)
        return df

    # [ ] TODO delete following method?
    # def duration_since_start(self, timestamp: datetime) -> float:
    #     """Duration since the start of the measurement to the timestamp

    #     Args:
    #         timestamp (datetime): arbitrary timestamp

    #     Returns:
    #         float: duration since the start of the measurement to the timestamp [s]
    #     """
    #     start_timepoint = self.read_start_timepoint()
    #     duration = timestamp - start_timepoint
    #     return duration.total_seconds()

    def read_measurement(self, measurement: int) -> pd.DataFrame:
        """Read pridb (Acoustic emission) data from one measurement

        Args:
            measurement (int): Number of the measurement to be read

        Raises:
            ValueError: The trai (transient data index) is for one channel not unique
            AttributeError: The first timepoint of the measurement data is smaller
                than the abs. timepoint of the measurement start

        Returns:
            pd.DataFrame: pridb (Acoustic emission) data of the measurement
        """
        channels = self.db.channel()
        parsed_markers = self.parse_markers()  # [ ] TODO maybe set the parsed markers as an
        # class attribute to avoid multiple read ins?
        # trai = (
        #     parsed_markers["Start TRAI"][measurement],
        #     parsed_markers["End TRAI"][measurement],
        # )
        time_start = parsed_markers["Start rel. [s]"][measurement]
        time_stop = parsed_markers["End rel. [s]"][measurement]
        # data = self.read(time_start=time_start, time_stop=time_stop)
        # set_id=trai-1 #usally
        trai_start = parsed_markers["Start TRAI"].iloc[measurement]
        trai_stop = parsed_markers["Stop TRAI"].iloc[measurement]
        data = self.read(set_id=list(range(trai_start - 1, trai_stop)))

        for ch in data.values():
            # it is not problematic if the start and stop trai of two
            # consecutive measurements are equal
            # the following check is just for security reasons
            if not ch.trai.is_unique:
                raise ValueError("The trais of the channel %i is not unique!" % ch.channel.iloc[0])
            if ch.time.iloc[0] < parsed_markers["Start rel. [s]"][measurement]:
                raise AttributeError(
                    "The first time entry in the measurement data is smaller than the time in the marker."
                )
            ch["Time rel. [s]"] = ch.time - parsed_markers["Start rel. [s]"][measurement]
        return data

    def read_measurement_own_markers(self, measurement: int) -> Dict[str, pd.DataFrame]:
        """Reads the specified measurment
        The measurement markers are in the own table Measurement Markers

        Args:
            measurement (int): number of the measurement to read

        Returns:
            Dict[str, pd.DataFrame]: Data of the measurement
        """
        markers = self.read_own_markers()
        # time_start = markers["Start rel. [s]"][measurement]
        # time_stop = markers["End rel. [s]"][measurement]
        # set_id=trai-1 #usally
        trai_start = markers["Start TRAI"].iloc[measurement]
        trai_stop = markers["Stop TRAI"].iloc[measurement]
        # data = self.read(time_start=time_start, time_stop=time_stop)
        data = self.read(set_id=list(range(trai_start - 1, trai_stop)))

        return data

    def insert_marker(self, time: float, set_type: int, data: str, number: Optional[int] = None) -> None:
        """Wrapper to generate an vae.io.MarkerRecord and write
        the MarkerRecord to the pridb

        Args:
            time (float): timepoint of the marker
            set_type (int): written in the ae_data
            data (str): text written in ae_markers (e.g. a timestamp, or
                "Start msu recording", ...)
            number (Union[int, None]): related to the kind of marker
                                        ( 1: first empty entry or start of the measurement,
                                          2: stop of the measurement)
        """
        self.db.write_marker(vae.io.MarkerRecord(time=time, set_type=set_type, data=data, number=number))

    def write_start_markers(self, measurement_start: datetime) -> None:
        """Writes the three start marker to the table ae_markers

        Args:
            measurement_start (datetime): timestamp of the measurement start
        """

        con = self.db.connection()
        cur = con.execute("SELECT Time FROM view_ae_data ORDER BY SetID DESC LIMIT 1")
        try:
            timemax = cur.fetchone()[0]  # None is not subscriptable -> TypeError
        except TypeError:
            timemax = 0
        # blocktime = blocksize / samplefrequency
        # time = blocktime + timemax
        # [ ] Review: rel time for the start markers not a complete blocktime, only the smallest timedelta
        time = 2e-9 + timemax
        self.insert_marker(time=time, set_type=6, data="", number=1)
        self.insert_marker(
            time=time,
            set_type=5,
            data=datetime_str(measurement_start),
            number=None,
        )
        self.insert_marker(
            time=time,
            set_type=4,
            data="Start msu recording",
            number=1,
        )

    def setid_to_trai(self, setid: int) -> int:
        """Return TRAI to given SetID

        Args:
            setid (int)

        Returns:
            int: corresponding TRAI to given SetID
        """
        variables_dict = {"setid": setid}
        sqlite3_file = PurePath(SQLITE3CODE_PATH, "get_trai_to_setid_pridb.sql")
        sqlite3code = SQLite3Code(file_obj=sqlite3_file)
        sqlite3code.assign_variables(variables_dict)
        result = sqlite3code.execute(self.db.connection())  # result is a list with one tuple as entry
        if result[0][0] != None:  # if result None, don't cast it to an integer
            trai = int(result[0][0])
        else:
            trai = None
        return trai

    def setid_to_time(self, setid: int) -> float:
        """Return time to given SetID

        Args:
            setid (int)

        Returns:
            float: corresponding time to given SetID
        """
        variables_dict = {"setid": setid}
        sqlite3_file = PurePath(SQLITE3CODE_PATH, "get_time_to_setid_pridb.sql")
        sqlite3code = SQLite3Code(file_obj=sqlite3_file)
        sqlite3code.assign_variables(variables_dict)
        result = sqlite3code.execute(self.db.connection())  # result is a list with one tuple as entry
        if result[0][0] != None:  # if result None, don't cast it to an integer
            time = float(result[0][0])
        else:
            time = None
        return time

    def write_label(self, label: str, timestamp: datetime) -> None:
        """Write a label to the pridb

        Args:
            label (str): Arbitrary string as label
            timestamp (datetime): timestamp, to which the label belongs
        """
        # TODO testen
        timedelta = self.duration_since_start(timestamp)
        self.insert_marker(
            time=timedelta, set_type=4, data=label, number=None
        )  # TODO check if the number should be different

    def set_all_sets_valid(self) -> None:
        """Set all sets in the pridb valid
        (writes the number of all sets in ae_globalinfo as number of ValidSets)"""

        sqlite3_file = PurePath(SQLITE3CODE_PATH, "get_last_setid_time_pridb.sql")
        sqlite3code = SQLite3Code(file_obj=sqlite3_file)
        result_list = sqlite3code.execute(self.db.connection(), raw=True)
        last_setid = result_list[0][0]  # last time not needed
        variables_dict = {"valid_sets": last_setid}
        sqlite3_file = PurePath(SQLITE3CODE_PATH, "update_validsets_pridb.sql")
        sqlite3code = SQLite3Code(file_obj=sqlite3_file)
        sqlite3code.assign_variables(variables_dict)
        sqlite3code.execute(self.db.connection())

    def write(self, hit_record: vae.io.pridb.HitRecord, samplefrequency: int, blocksize: int) -> None:
        """Wrapper for pridb write hit """
        # [ ] TODO check if that is correct in case of not continuos measurement!
        con = self.db.connection()
        cur = con.execute("SELECT Time FROM view_ae_data ORDER BY SetID DESC LIMIT 1")
        try:
            timemax = cur.fetchone()[0]  # None is not subscriptable -> TypeError
        except TypeError:
            timemax = 0
        blocktime = blocksize / samplefrequency
        if hit_record.time + 1e-9 > timemax:
            self.db.write_hit(hit_record)
        else:
            time = blocktime + timemax  # [ ] TODO in hit based mode?
            amplitude = hit_record.amplitude
            channel = hit_record.channel
            duration = hit_record.duration
            energy = hit_record.energy
            paramid = hit_record.param_id
            rms = hit_record.rms
            trai = hit_record.trai
            signalstrength = hit_record.signal_strength
            hit_record = vae.io.HitRecord(
                time=time,
                channel=channel,
                param_id=paramid,
                amplitude=amplitude,
                duration=duration,
                energy=energy,
                rms=rms,
                signal_strength=signalstrength,
                trai=trai,
            )

            self.db.write_hit(hit_record)

    def determine_write_ae_params(self, config: pd.DataFrame) -> None:
        """Wrapper function to determine the ae_params with the config of the
        measurement and write them in the pridb

        Args:
            config (pd.DataFrame): Measurement configuration
        """

        ae_params = get_ae_params(config)
        self.write_ae_params(ae_params)

    def write_ae_params(self, ae_params: pd.DataFrame) -> None:
        """Write the ae_params in the pridb

        Args:
            ae_params (pd.DataFrame): current layout:
               ID  SetupID  Chan    ADC_µV    ADC_TE    ADC_SS
                1   1        1     0  0.000000  0.000000  0.000000
                2   2        1     1  1.677338  0.000113  0.000671
                3   3        1     2  0.053042  0.000281  0.053042

        """
        engine = sa.create_engine(f"sqlite:///{self.path}")
        ae_params.to_sql("ae_params", engine, if_exists="replace")

    def read_ae_params(self) -> Dict[str, Any]:
        """Reads the ae parameters from the pridbfile

        Returns:
            [Dict]: AE-parameters
        """
        # [ ] TODO candidate for abstract parent method
        self.ae_params = self.db._parameter_table()
        return self.ae_params

    def get_last_trai(self) -> int:
        """Reads the last trai

        Returns:
            int: last trai written in the pridb
        """
        sqlite3_file = PurePath(SQLITE3CODE_PATH, "get_last_trai_pridb.sql")
        sqlite3code = SQLite3Code(file_obj=sqlite3_file)
        result_list = sqlite3code.execute(self.db.connection(), raw=True)
        if len(result_list) > 0:
            last_trai = result_list[0][0] if result_list[0][0] else 1
        else:
            last_trai = 1

        return last_trai

    def write_stop_marker(self, samplefrequency: int) -> None:
        """Writes the stop marker to the table ae_markers

        Args:
            samplefrequency (int): samplefrequency used for the measurement

        """
        timestop = datetime.now()

        sqlite3_file = PurePath(SQLITE3CODE_PATH, "get_last_setid_time_pridb.sql")
        sqlite3code = SQLite3Code(file_obj=sqlite3_file)
        result_list = sqlite3code.execute(self.db.connection(), raw=True)
        last_time = result_list[0][1]
        last_time = last_time / samplefrequency
        self.insert_marker(
            time=last_time,
            set_type=5,
            data=datetime_str(timestop),
            number=None,
        )
        self.insert_marker(
            time=last_time,
            set_type=4,
            data="Stop recording",
            number=2,
        )

    def close(self) -> None:
        """Wrapper to close the pridb"""
        self.db.close()
