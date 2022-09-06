"""Read tradb files"""  # [ ] TODO@KB,AH Create an abstract vaedb class

import logging
import os
from datetime import datetime
from pathlib import Path, PurePath
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
import sqlalchemy as sa
import vallenae as vae
from vallendb import BaseFile, SQLite3Code
from vallenae.io.datatypes import TraRecord
from vallenae.io.tradb import TraDatabase
from vallenae.io.types import SizedIterable

from vallendb.utils import (
    get_tr_params,
    read_acq_settings,
    set_filestatus,
    set_timebase,
    store_acq_settings,
    write_guid,
)

LOGGER = logging.getLogger(__name__)
SQLITE3CODE_PATH = os.path.join(Path(__file__).resolve().parent, "sqlite3_code")


class TradbFile(BaseFile):
    """Special File Operations"""

    # [x] TODO Add context manager functionality: __enter__ and __exit__ method
    # [x] TODO remove the connection wrapper
    # [ ] TODO maybe add a posibility to filter the data afterwards, downsample, .. or leave that in vaspy?
    def __init__(
        self,
        file_obj: PurePath,
    ):
        """Inherit all attributes and methods from the BaseFile Class

        Args:
            file_obj (PurePath): filename and location"""
        super().__init__(file_obj)
        self._check_filetypes((".tradb",))
        self.table_prefix = "tr"
        self.mode = str()
        self.compression = bool()
        self.db = TraDatabase
        self.tr_params = dict()
        self.channels = dict()
        self.data = pd.DataFrame()

    # call is needed to pass arguments to the enter function
    def __call__(self, mode: str = "ro", compression: bool = True):
        """context manager function to pass arguments to the enter function

        Args:
            mode (str, optional): Mode of the database connection: "ro": read-only
                                    "rw": read-write
                                    "rwc": read-write-create
                                    Defaults to "ro".
            compression (bool, optional): de-/activate compression of the transient data
                                        Only relevant, if writing data to the database

        Returns:
            [type]: pass the class instance to the enter method
        """
        self.mode = mode
        self.compression = compression
        return self

    def __enter__(
        self,
    ) -> vae.io.TraDatabase:
        """Connects to the database in an with-statement

        Returns: TradbFile object of the specified tradb
        """

        self.db = vae.io.TraDatabase(filename=self.path, mode=self.mode, compression=self.compression)

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
        """Create a vallenae transient database.
        Args:
            config (pd.DataFrame): Measurement configuration
        """

        set_timebase(self.db, config.loc[1:, "Samplefrequency"].astype(np.int32).max())
        self.set_tr_params(config)
        store_acq_settings(self.path, config)
        write_guid(self)

    def read_original_format(self, **kwargs: dict) -> pd.DataFrame:
        """read transient data in the original format (channel data alterning)

        Returns:
            pd.DataFrame: transient data (not sorted by channel)
        """
        data = self.db.read(**kwargs)
        self.data = data
        return data

    def read(
        self,
        **kwargs: dict,
    ) -> Dict:
        """Load a file.

        channel: None if all channels should be read.
                Otherwise specify the channel number or a list of channel numbers
        time_start: Start reading at relative time (in seconds). Start at beginning if `None`
        time_stop: Stop reading at relative time (in seconds). Read until end if `None`
        trai: Read data by TRAI (transient recorder index)
        query_filter: Optional query filter provided as SQL clause,
                e.g. "Pretrigger == 500 AND Samples >= 1024"

        Returns: A pandas dataframe

        """
        data = self.read_original_format(**kwargs)
        self.channels = {f"CH{name}": x for name, x in data.groupby("channel")}
        # if kwargs and ("trai" in kwargs.keys()): # [ ] TODO@KB Create a table for all settings e.g. channel sensor name = VS150M
        #     trai = kwargs["trai"]
        #     self.settings = self.get_settings(trai=trai)

        return self.channels

    def iread(self, **kwargs: dict) -> SizedIterable[TraRecord]:
        """Wrapper for the iread of the tradb

        Returns:
            SizedIterable[TraRecord]:
        """
        return self.db.iread(**kwargs)

    def read_trai_range(self, trai_start: int, trai_stop: int) -> pd.DataFrame:
        """Reads measurement data by specified trai range
        Also handles overlapping trai ranges of consecutive measurements [ ] TODO should be obsolent in the future

        Args:
            trai_start (int): start trai index of the range (inclusive)
            trai_stop (int): stop trai index of the range (inclusive)

        Returns:
            pd.DataFrame: transient data in the specified trai range
        """
        data = self.read_original_format(trai=range(trai_start, trai_stop + 1))
        # check if there are more multiple trai entries than channels
        # [ ] TODO this dropping of overlapping trais of consecutive measurements, should
        # be obsolent after an update of the measurement interface ( also an TODO)
        # [ ] TODO this slicing may be wrong if there are not twice data entries than channels
        # like 2 entries with the same trai for channel 1, but only one entry with that trai for channel 2
        channels = len(data.channel.unique())
        trai_check = data.index.value_counts() > channels
        if trai_check.any():
            # the following checks have to be done before the reset index!
            # check if the multiple entries are at the start
            trai_start_check = (data[trai_check].index == trai_start).any()
            # or at the end (different if statements, because both can be true at the same time)
            trai_stop_check = (data[trai_check].index == trai_stop).any()
            data = data.reset_index()
            if trai_start_check:
                # drop the channel entries of the previous measurement
                data = data.drop(data.index[range(0, channels)])
            if trai_stop_check:
                # drop the channel entries of the next measurement
                data = data.drop(data.index[range(-channels, 0)])
            data = data.set_index("trai")
        self.data = data
        return data

    def set_tr_params(self, config: pd.DataFrame) -> None:
        """Set the tr parameters in the tradb, depending to the config of the measurement

        Args:
            config (pd.DataFrame): configuration of the measurement

        """
        tr_params = get_tr_params(config)
        engine = sa.create_engine(f"sqlite:///{self.path}")
        tr_params.to_sql("tr_params", engine, if_exists="replace")

    def get_measurement_duration(self) -> float:
        """reads the measurement duration [s] from a tradb

        Returns:
            float: measurement duration [s]
        """

        sqlite3_code_path = PurePath(SQLITE3CODE_PATH, "get_last_timepoint_tradb.sql")
        sqlite3code = SQLite3Code(file_obj=sqlite3_code_path)
        result_list = sqlite3code.execute(self.db.connection(), raw=True)
        measurement_duration = float(result_list[0][0])
        return measurement_duration

    def get_measurement_start_timepoint(
        self,
    ) -> datetime:  # TODO Check if necessary/correct
        # Use start timepoint from the pridb instead!!
        """calculates the the timepoint of the measurement start with the data from a tradb

        Args:
            self ([tradbfile]):

        Returns:
            measurement_start (datetime): start of the tradb measurement

        """
        tradb_completion_time = os.stat(self.path).st_mtime
        mesurement_duration = self.get_measurement_duration()
        measurement_start = datetime.fromtimestamp(tradb_completion_time - mesurement_duration)

        return measurement_start

    def get_first_time_trai(
        self,
    ) -> Tuple[
        float, int
    ]:  # [ ] TODO delete this function and use get_first_last_trai from utils? Or is the result different?

        (t_start, _) = self.db._get_total_time_range()
        trai_start, _ = self.db._get_trai_range_from_time_range(t_start)

        return (t_start, trai_start)

    def get_last_time_trai(
        self,
    ) -> Tuple[
        float, int
    ]:  # [ ] TODO delete this function and use get_first_last_trai from utils? Or is the result different?

        (_, t_stop) = self.db._get_total_time_range()
        if t_stop != 0:
            # following code returns instead of the last trai one trai before the last one!
            # _, trai_stop = self.db._get_trai_range_from_time_range(None, t_stop)
            sqlite3_code_path = PurePath(SQLITE3CODE_PATH, "get_last_trai_tradb.sql")
            sqlite3code = SQLite3Code(file_obj=sqlite3_code_path)
            result_list = sqlite3code.execute(self.db.connection(), raw=True)
            trai_stop = int(result_list[0][0])
        else:
            trai_stop = 0

        return (t_stop, trai_stop)

    def get_settings(self, trai: Optional[int] = None) -> Dict[str, float]:
        """Reads the measurement settings of the first row in the table tr_data
            (should be the same than in the table acq_settings)

        Returns:
            Dict[str, float]: [description]
        """
        if trai:
            data = vae.io.iter_to_dataframe(self.db.iread(channel=None, time_start=None, time_stop=None, trai=trai))
        else:
            data = vae.io.iter_to_dataframe(self.db.iread(channel=None, time_start=None, time_stop=None, trai=1))
        settings = {}
        settings["Pretrigger"] = data["pretrigger"].iloc[0]
        settings["Threshold"] = data["threshold"].iloc[0]
        settings["Samplefrequency"] = data["samplerate"].iloc[0]
        settings["Blocksize"] = data["samples"].iloc[0]
        settings["Compression"] = True if data["data_format"].iloc[0] == 2 else False

        return settings

    # def write_start_lines(
    #     self, samplefrequency: int, blocksize: int, compression: bool
    # ) -> None:
    #     # TODO necessary?
    #     if compression:
    #         self.tradb.write(
    #             vae.io.tradb.TraRecord(
    #                 0.0,
    #                 1,
    #                 3,
    #                 0,
    #                 0.0,
    #                 samplefrequency,
    #                 blocksize,
    #                 np.random.rand(blocksize),
    #                 1,
    #             )
    #         )
    #         self.tradb.write(
    #             vae.io.tradb.TraRecord(
    #                 0.0,
    #                 2,
    #                 3,
    #                 0,
    #                 0.0,
    #                 samplefrequency,
    #                 blocksize,
    #                 np.random.rand(blocksize),
    #                 2,
    #             )
    #         )
    #     else:
    #         self.tradb.write(
    #             vae.io.tradb.TraRecord(
    #                 0.0,
    #                 1,
    #                 3,
    #                 0,
    #                 0.0,
    #                 samplefrequency,
    #                 blocksize,
    #                 np.random.rand(blocksize),
    #                 1,
    #             )
    #         )
    #         self.tradb.write(
    #             vae.io.tradb.TraRecord(
    #                 0.0,
    #                 2,
    #                 3,
    #                 0,
    #                 0.0,
    #                 samplefrequency,
    #                 blocksize,
    #                 np.random.rand(blocksize),
    #                 2,
    #             )
    #         )

    def write(self, tra_record: vae.io.tradb.TraRecord, compression: bool = True) -> None:
        """Wrapper for tradb write

        Args:
            tra_record (vae.io.tradb.TraRecord): transient record to write in the tradb

        Compression (flac-compression) is de-/activated by the connection to the .pridb
        If using the context-manager the mode and the compression (bool) are selectable
        """
        self.db.write(tra_record)

    def read_tr_params(self) -> Dict[str, Any]:
        """Reads the tr parameters from the tradbfile

        Returns:
            [Dict]: TR-parameters
        """
        # [ ] TODO candidate for abstract parent method
        self.tr_params = self.db._parameter_table()
        return self.tr_params

    def close(self) -> None:
        """ "Wrapper for tradb close

        Sometimes necessary"""

        self.db.close()
