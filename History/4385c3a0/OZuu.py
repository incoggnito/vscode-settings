import logging
import os
from pathlib import Path, PurePath
from typing import Any, Dict, Optional, Sequence, Union

# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import vallenae as vae

# import vaspy
from vallendb import BaseFile, SQLite3Code
from vallenae.io.trfdb import TrfDatabase

from vallendb.utils import (
    set_filestatus,
    store_acq_settings,
    write_guid,
)

logger = logging.getLogger(__name__)
SQLITE3CODE_PATH = PurePath(Path(__file__).resolve().parent, "sqlite3_code")


class TrfdbFile(BaseFile):
    """Special File Operations"""

    # [x] TODO Add context manager functionality: __enter__ and __exit__ method
    # [x] TODO remove the connection wrapper
    def __init__(self, file_obj: PurePath):  # , timebase: int, mode: str = "ro"):
        """Inherit all attributes and methods from the BaseFile Class

        Args:
            file_obj (PurePath): filename and location"""
        super().__init__(file_obj)
        self._check_filetypes((".trfdb",))
        self.table_prefix = "trf"
        self.db = TrfDatabase
        self.mode = str()
        self.data = pd.DataFrame()

    def __call__(self, mode: str = "ro") -> BaseFile:
        # [ ] TODO is the return type annotation "BaseFile" correct? TrfdbFile is not possible
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
    ) -> vae.io.TrfDatabase:
        """Connects to the database in an with-statement

        Returns:
            vae.io.TrfDatabase: TrfDatabase object of the specified trfdb
        """
        self.db = vae.io.TrfDatabase(filename=self.path, mode=self.mode)
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
        if self.mode in ["rwc", "rw"]:
            set_filestatus(self.db, 0)
        self.db.close()

    def create(self, config: pd.DataFrame) -> None:
        """Creates a trfdb and writes the file id (guid)"""
        write_guid(self)
        store_acq_settings(self.path, config)

    def iread(
        self,
        trai: Union[None, int, Sequence[int]] = None,
        query_filter: Optional[str] = None,
    ) -> pd.DataFrame:
        """Wrapper of the stream features with returned iterable.
        Args:
            trai: Read data by TRAI (transient recorder index)
            query_filter: Optional query filter provided as SQL clause,
                e.g. "FFT_CoG >= 150 AND CTP < 20"

        Returns: A pandas dataframe

        """
        # [ ] REVIEW if that function is necessary
        datagenerator = self.db.iread(trai=trai, query_filter=query_filter)
        temp_data = pd.DataFrame(datagenerator)
        data = pd.DataFrame()
        if not temp_data.empty:
            data = pd.json_normalize(temp_data.features)
            data = data.set_index(temp_data.trai)
        self.data = data
        return self.data

    def read(
        self,
        **kwargs: dict,
    ) -> pd.DataFrame:
        """Load a file.

        trai: Read data by TRAI (transient recorder index)
        query_filter: Optional query filter provided as SQL clause,
                e.g. "Pretrigger == 500 AND Samples >= 1024"

        Returns: A pandas dataframe

        """
        data = self.db.read(**kwargs)
        if "Time" in data.columns:
            # [ ] Review is this relative time correct?
            data["Time rel. [s]"] = data["Time"] - data["Time"].iloc[0]
        self.data = data
        return self.data

    def read_fieldinfo(self) -> Dict[str, Dict[str, Any]]:
        """Reads the fieldinfo (units and other column-related meta data)

            Units and other column-related meta data is saved in the `trf_fieldinfo` table
            Visual AE needs that information. Otherwise it is not possible to visualize own features with Visual AE.

        Returns:
            Dict[str, Dict[str, Any]]: fieldinfo
        """

        fieldinfo = Dict(self.db.fieldinfo())
        return fieldinfo  # typing: ignore

    def write(self, features: Dict) -> None:
        """Write features in trfdb Database

        If the entry (with the given trai) already exists, it is going to be overwritten

        Args:
            features (Dict): necessary keys: Time, Channel, TRAI
                and additional all features to write"""
        # [ ] TODO die features auch als int16 abspeichern (genauso wie die pridb-Werte und tradb-Werte)
        # [ ] TODO feature range factors berechnen
        # feature_set = vae.io.FeatureRecord(
        #     trai=tra.trai,
        #     # {f"{f_name}": self.feature_func_handler(f_func, *f_args, tra) for f_name,f_func, *f_args in acv_features.items()},
        #     features=feat,
        # )
        # for trai, (_, row) in enumerate(features.iterrows(), 1):
        trai = features.pop("TRAI")
        feature_set = vae.io.FeatureRecord(trai, features)
        self.db.write(feature_set)

    def write_fieldinfo(self, field: str, fieldinfo: Dict) -> None:
        """Units and other column-related meta data is saved in the `trf_fieldinfo` table
        Visual AE needs that information. Otherwise it is not possible to visualize own features with Visual AE.

        Args:

            field (str): field info for which feature
            fieldinfo (Dict): "Unit": e.g. kHz, mV, micros
                              "LongName": long name of the feature
                              "Description" (optional)
                              "ShortName": (optional)
                              "FormatStr": (optional) # [ ]TODO meaning of that variable

        Examples:

        - write_fieldinfo("ATO_Hinkley", {"Unit": "[µs]", "LongName": "Arrival Time Offset (Hinkley)"})
        - write_fieldinfo("ATO_AIC", {"Unit": "[µs]", "LongName": "Arrival Time Offset (AIC)"})
        - write_fieldinfo("ATO_ER", {"Unit": "[µs]", "LongName": "Arrival Time Offset (ER)"})
        - write_fieldinfo("ATO_MER", {"Unit": "[µs]", "LongName": "Arrival Time Offset (MER)"})
        """

        self.db.write_fieldinfo(field, fieldinfo)

    def get_last_trai(self) -> int:
        """Reads the last trai

        Returns:
            int: last trai written in the pridb
        """
        sqlite3_file = PurePath(SQLITE3CODE_PATH, "get_last_trai_trfdb.sql")
        sqlite3code = SQLite3Code(file_obj=sqlite3_file)
        result_list = sqlite3code.execute(self.db.connection(), raw=True)
        last_trai = result_list[0][0]

        return last_trai

    def close(self) -> None:
        """Wrapper to close the database"""
        self.db.close()

    # def generate_plots(self, nr_channels: int, save: bool, outputtype: str) -> None:
    #     # TODO evtl. dieses Funktion wieder entfernen! Evtl. eher die jeweiligen Projekte, wo die Daten ausgewertet werden sollen, bspw. in SmartSAD, ...
    #     # TODO oder in das Projekt Fyrsonic oder evlt. in das noch nicht existierende Projekt ConditionWave
    #     """Generate plots of all features in the feature-database trfdb

    #     Args:
    #         trfdb (TrfdbFile):
    #         nr_channels (int): Number of channels of the original tradb, it is asumend that the features are ordered blockwise by time (like row 1: ch1 and timepoint 1, row 2: ch2 and tp 1, row 3: ch1 and tp 2, row 4: ch2 and tp 2, ...)
    #     """
    #     dir = self.dir
    #     name = self.name

    #     save_str = os.path.join(dir, name)

    #     trfdb_df = self.read()
    #     for ch in range(nr_channels):
    #         df_ch = trfdb_df.iloc[ch::nr_channels]
    #         for i in df_ch.columns:
    #             featurename = f"_{ch+1}_{i}"
    #             exportname = save_str + featurename
    #             # trfdb_df[i].plot(
    #             #    title=f"{name} {i} -  Channel: {ch+1}",
    #             #    xlabel="Block Number",
    #             #    figsize=(17, 8),
    #             # )
    #             title = f"{name} - {i} - Channel: {ch+1}"
    #             x = np.arange(len(trfdb_df[i]))
    #             fig2, ax21 = plt.subplots()
    #             ax21.scatter(x=x, y=trfdb_df[i], marker=".", s=0.5)
    #             # ax21.set_yscale("log") #TODO set default log and lin for the different features
    #             ax21.set_xlabel("Blocknummer")
    #             ax21.grid()
    #             ax21.set_title(title)
    #             ax21.set_ylabel(i)

    #             if save and outputtype == "png":
    #                 plt.savefig(exportname + ".png")
    #                 plt.clf()
    #             elif save and outputtype == "svg":
    #                 plt.savefig(exportname + ".svg")
    #                 plt.clf()
    #             else:
    #                 plt.show()


# # %%
# if __name__ == "__main__":
#     # subdir = (
#     #     r"data\Measurements\2021_April_Kieselstein\2021-04-26_Baustahl\Gesund_keine_30"
#     # )
#     # filename = "keine_Fyrsonic"
#     # filename_tradb = filename + ".tradb"
#     # filepath_tradb = PurePath(os.path.join(subdir, filename_tradb))
#     config = {
#         "Channel": "All channels same settings",
#         "MeasurementMode": "Streaming",
#         "Range": "50 mV",
#         "PreamplifierGain": "0 dB",
#         "Samplefrequency": 2500000,
#         "Filter-LowerLimit": 0,
#         "Filter-UpperLimit": 1000,
#         "Blocksize": 65536,
#     }
#     subdir = r"data\Measurements\Test"
#     filename = "Test.tradb"
#     filepath_tradb = PurePath(subdir, filename)
#     tradb_file = TradbFile(filepath_tradb, config)
#     bandwidth = 65536
#     data = tradb_file.read_original_format()
#     settings = tradb_file.get_settings()
#     # feature_selection = ["Mean", "ATO_Hinkley", "FFT_Mean"]
#     features = vaspy.feature.calculation.feature_calculation(
#         data["data"],
#         settings["Samplefrequency"],
#         settings["Pretrigger"],
#         feature_selection=["All"],
#     )
#     print("Feature calculation successfully completed.")
#     filename = "Test.trfdb"
#     filepath = PurePath(subdir, filename)
#     trfdb_file = TrfdbFile(filepath, mode="rwc")
#     trfdb_file.write(features)
#     # nr_channels = (
#     #     2  # it is also possible to get the number of channels from the tradb file
#     # )
#     # save = False
#     # outputtype = "png"
#     # trfdb_file.generate_plots(
#     #     nr_channels=nr_channels, save=save, outputtype=outputtype
#     # )  # TODO dickere plot Punkte #TODO data selction wie in matlab (um trai herauszufinden!)
#     trfdb_file.close()
#     print("All successfully done.")

# # #%%
# # # Show results as table:
# # print(pd.DataFrame(trfdb.fieldinfo()))


# # print(pd.DataFrame(trfdb.fieldinfo()).filter(regex="ATO"))

# # #%%
# # # Load results in VisualAE
# # # ~~~~~~~~~~~~~~~~~~~~~~~~
# # # Time arrival offsets can be specified in the settings of `Location Processors` - `Channel Positions` - `Arrival Time Offset`.
# # # (Make sure to rename the generated trfdb to match the filename of the pridb.)
# # #
# # # .. image:: /images/vae_arrival_time_offset.png

if __name__ == "__main__":
    subdir = r"data\Measurements\Test"
    filename = "Test.trfdb"
    timebase = 1000000
    filepath = PurePath(subdir, filename)
    trfdb_file = TrfdbFile(filepath)
