"""Handle mf4files files"""

import logging
from pathlib import PurePath, Path
from typing import Dict, Generator, List, Tuple
from asammdf import MDF
from asammdf.blocks.utils import MdfException  # this exception class is not very usefull
import collections

import numpy as np
import pandas as pd

from .utils import BaseFile, Data

LOGGER = logging.getLogger(__name__)


class Mf4File(BaseFile):
    """Special Operations on mf4 files"""

    def __init__(self, file_obj: PurePath):
        """Inherit all attributes and methods from the _File Class

        supported file formats:
            'mf4':    mf4 files


        """
        super().__init__(file_obj)
        self._check_filetypes((".mf4",))
        self.data = Data
        self.samplefrequency = float()
        self.samples = int()  # [ ] TODO empty init of variable type so okay?
        self.data.x = np.array([])

    def read(
        self, channels: List[int] = [], skip_normal_mode: bool = False, ignore_size_warning: bool = False
    ) -> pd.DataFrame:
        """Reads the mf4 file.
        It is possible to read compressed files.

        Args:
            channels (List[int]): list of channels to read. Defaults to [].
                -> Reading all channels
            skip_normal_mode (bool): If you already know, that some channels throw Exceptions you can skip
                the asammdf.to_dataframe() method to save some time and read all available channels to a
                dataframe. Defaults to False.
            ignore_size_warning (bool): Set this parameter to true if you want to try joining all Data
                despite the size warning. (can be very slow). Defaults to False.

        Returns:
            pd.DataFrame: data of the mf4 file"""

        successfull = False
        LOGGER.info("Reading of the mf4 file started.")
        if len(channels) == 0:
            mdf_obj = MDF(self.path)
        else:
            mdf_obj = MDF(self.path, channels=channels)
            LOGGER.info(f"Started reading the following channels : {channels}")

        if not skip_normal_mode:
            try:
                result = mdf_obj.to_dataframe()
                successfull = True
            except Exception as error:
                LOGGER.warning(f"asammdf MDF.to_dataframe() function had this error: {error}")
                LOGGER.info("Now trying to read all possible channels.")
                successfull = False
        if not successfull:
            # Review type of st_size
            # check if size is bigger than 200 MB
            if int(Path(self.path).stat().st_size / 1e6) >= int(200) and not ignore_size_warning:
                LOGGER.warning("File Size of the original .mf4 file is too big to concat it with pandas in RAM.")
                LOGGER.info("Use save_mf4_to_parquet_file or set try_despite_size_warning to True (not recommended).")
                result = pd.DataFrame()
            else:

                valid_channels = self.check_channels()

                mdf_obj = MDF(self.path, channels=valid_channels)
                # Review if defaultdict is needed
                dict_df = collections.defaultdict(list)
                LOGGER.info("Loading remaining channels to DataFrame ...")
                for channel in range(len(mdf_obj.groups)):
                    temp_df = mdf_obj.get_group(channel)
                    if len(temp_df) == 0:
                        continue
                    else:
                        key = str(len(temp_df))
                        dict_df[key].append(temp_df)

                LOGGER.info("Joining resulting DataFrames to one pandas.DataFrame ...")
                final_list = []
                # [ ] Review the following code
                for key in dict_df:
                    temp_list = dict_df[key]
                    temp_df_one = temp_list[0]
                    for i in range(len(temp_list) - 1):
                        temp_df_two = temp_list[i + 1]
                        column_list = list(temp_df_two.columns)
                        for col in column_list:
                            temp_df_one[col] = temp_df_two[col]
                    final_list.append(temp_df_one)

                result = pd.concat(final_list, axis=1)
                LOGGER.info("Reading mf4 file done.")

        return result

    def check_channels(self) -> List[str]:
        """Check all channels in data so look for errors

        Returns:
            List[str]: Channels, which can be load from the mf4file
        """

        mdf_obj = MDF(self.path)
        mdf_columns = set(list(mdf_obj.channels_db.keys()))
        available_channels = []
        LOGGER.info("Checking available channels ...")
        for group in range(len(mdf_obj.groups)):
            try:
                # [ ] Review that get_group already loads data!
                temp_df = mdf_obj.get_group(index=group)
                available_channels = available_channels + list(temp_df.columns)
                continue
            except Exception as error:
                LOGGER.warning(f"asammdf MDF.to_dataframe() function had this error: {error}")
                LOGGER.info("Now trying to read all possible channels.")
                continue

        duplicated_channels = [item for item, count in collections.Counter(available_channels).items() if count > 1]
        available_channels = list(set(available_channels) - set(duplicated_channels))
        unavailable_channels = list(set(mdf_columns).difference(set(available_channels)))

        LOGGER.info(
            "These channels cause errors when reading the file due to array mismatches or duplications in the channel names: ",
            unavailable_channels,
        )
        return available_channels

    def get_header(self) -> Dict:

        mdf_obj = MDF(self.path)
        keys = mdf_obj.header.__slots__
        self.header = {key: mdf_obj.header[key] for key in keys}
        self.doc = mdf_obj.header.__doc__
        self.start_time = mdf_obj.start_time

        return self.header

    def get_all_units(self) -> List[Dict]:
        mdf_obj = MDF(self.path)
        sensor_groups = []
        for g in mdf_obj.groups:
            units = {}
            units["acq_name"] = g.channel_group.acq_name
            for ch in g.channels:
                units[ch.name] = ch.unit
            sensor_groups.append(units)

        self.units = sensor_groups
        return self.units

    def parse_events(self) -> List:

        mdf_obj = MDF(self.path)
        self.events = [i.comment for i in mdf_obj.events]

        return self.events

    def get_df_iterator(self, **kwargs) -> Generator:
        """yields 200MB dataframes
        If the resulting dataframe is less than 200MB the generator has only one entry.

        Returns:
            [Generator]: generator with 200MB dataframes
        """
        mdf_obj = MDF(self.path)
        if "channels" in kwargs.keys():
            # convert single str to list with one string
            if isinstance(kwargs["channels"], str):
                kwargs["channels"] = [kwargs["channels"]]
        return mdf_obj.iter_to_dataframe(**kwargs)

    # def write(self, data: pd.DataFrame) -> None:
    #     """Use this funtion to save your .mf4 file as a .parquet file.

    #     :param filename: The filename of your .mf4 file.
    #     :type filename: str
    #     :param filepath: The path to the folder where your .mf4 data is stored.
    #     :type filepath: str
    #     :return: There is no return type the function creates the .parquet folder.
    #     :rtype: None

    #     """
    #     temp_folder = str(randint(10000, 99999))
    #     if not os.path.exists(temp_folder):
    #         os.makedirs(temp_folder)
    #         print("Creating necessary directories for this function: " + temp_folder + "/")

    #     if not os.path.exists("parquet"):
    #         os.makedirs("parquet")
    #         print("Creating necessary directories for this function: parquet/")

    #     print("Reading " + filepath + filename + " started.")
    #     mdf_obj = MDF(filepath + filename)
    #     mdf_columns = set(list(mdf_obj.channels_db.keys()))

    #     available_channels = []
    #     print("Selecting available channels ...")
    #     for group in tqdm(range(len(mdf_obj.groups))):
    #         try:
    #             temp_df = mdf_obj.get_group(index=group)
    #             available_channels = available_channels + list(temp_df.columns)
    #             continue
    #         except:
    #             continue

    #     duplicated_channels = [item for item, count in collections.Counter(available_channels).items() if count > 1]
    #     available_channels = list(set(available_channels) - set(duplicated_channels))
    #     unavailable_channels = list(set(mdf_columns).difference(set(available_channels)))

    #     print(
    #         "These channels cause errors when reading the file due to array mismatches or duplications in the channel names: ",
    #         unavailable_channels,
    #     )

    #     mdf_obj = MDF(filepath + filename, channels=available_channels)
    #     dict_df = defaultdict(list)
    #     print("Loading remaining channels to DataFrame ...")
    #     for channel in tqdm(range(len(mdf_obj.groups))):
    #         temp_df = mdf_obj.get_group(channel)
    #         if len(temp_df) == 0:
    #             continue
    #         else:
    #             key = str(len(temp_df))
    #             dict_df[key].append(temp_df)

    #     print("Joining resulting DataFrames with same length to one pandas.DataFrame ...")
    #     final_list = []
    #     for key in dict_df:
    #         temp_list = dict_df[key]
    #         temp_df_one = temp_list[0]
    #         for i in range(len(temp_list) - 1):
    #             temp_df_two = temp_list[i + 1]
    #             column_list = list(temp_df_two.columns)
    #             for col in column_list:
    #                 temp_df_one[col] = temp_df_two[col]
    #         final_list.append(temp_df_one)

    #     print("Writing remaining DataFrames as .parquet to " + temp_folder + "/ ...")
    #     list_temp_files = []
    #     longest_temp_dataframe = 0
    #     longest_temp_dataframe_path = ""
    #     try:
    #         for i in tqdm(range(len(final_list))):
    #             if len(final_list[i]) >= longest_temp_dataframe:
    #                 longest_temp_dataframe = len(final_list[i])
    #                 longest_temp_dataframe_path = temp_folder + "/pt" + str((i + 1)) + ".parquet"
    #             write_dataframe_to_parquet(df=final_list[i], name="pt" + str((i + 1)), path=temp_folder + "/")
    #             list_temp_files.append(temp_folder + "/pt" + str((i + 1)) + ".parquet")
    #         list_temp_files.remove(longest_temp_dataframe_path)
    #         print("Writing remaining DataFrames as .parquet to " + temp_folder + "/ done.")
    #     except Exception as error:
    #         print("Write temp .parquet failed with this exception: ", error)

    #     system_ram = int(psutil.virtual_memory().total / (1024 ** 3))
    #     print("Starting Spark session.")
    #     spark = SparkSession.builder.config("spark.driver.memory", str(system_ram) + "g").getOrCreate()
    #     print("Spark Session started with these configs:", SparkConf().getAll())
    #     print(
    #         "To monitor your spark Session open this link in your browser: ",
    #         spark.sparkContext.uiWebUrl,
    #     )

    #     del final_list
    #     del mdf_obj
    #     del dict_df
    #     del available_channels
    #     del unavailable_channels
    #     del duplicated_channels
    #     del mdf_columns

    #     files_to_delete = list_temp_files.copy()
    #     list_spark_df = [None] * len(list_temp_files)
    #     longest_dataframe = spark.read.parquet(longest_temp_dataframe_path)
    #     longest_dataframe.sort("timestamps").coalesce(len(longest_dataframe.columns)).write.mode("overwrite").parquet(
    #         temp_folder + "/" + filename[:-4] + longest_temp_dataframe_path[-11:]
    #     )
    #     files_to_delete.append(temp_folder + "/" + filename[:-4] + longest_temp_dataframe_path[-11:])
    #     longest_dataframe = spark.read.parquet(longest_temp_dataframe_path)

    #     print("Reading " + temp_folder + "/ .parquets to spark DataFrames ...")
    #     for i in tqdm(range(len(list_temp_files))):
    #         list_spark_df[i] = spark.read.parquet(list_temp_files[i])
    #         list_spark_df[i].sort("timestamps").coalesce(len(list_spark_df[i].columns)).write.mode("overwrite").parquet(
    #             temp_folder + "/" + filename[:-4] + list_temp_files[i][-11:]
    #         )
    #         files_to_delete.append(temp_folder + "/" + filename[:-4] + list_temp_files[i][-11:])
    #         list_spark_df[i] = spark.read.parquet(list_temp_files[i])
    #     print("Reading " + temp_folder + "/ .parquets to spark DataFrames done.")

    #     print("Joining spark DataFrames ...")
    #     for i in tqdm(range(len(list_spark_df))):
    #         longest_dataframe = longest_dataframe.join(list_spark_df[i], ["timestamps"], "fullouter")
    #     print("Joining spark DataFrames done.")

    #     print("Writing final DataFrame to parquet/" + filename[:-4] + ".parquet ...")
    #     longest_dataframe.sort("timestamps").coalesce(len(longest_dataframe.columns)).write.mode("overwrite").parquet(
    #         "parquet/" + filename[:-4] + ".parquet"
    #     )
    #     print("Writing final DataFrame to parquet/" + filename[:-4] + ".parquet done.")
    #     spark.stop()

    #     print("Removing " + temp_folder + "/ folder ...")
    #     try:
    #         shutil.rmtree(temp_folder)
    #     except Exception as error:
    #         print(error)
    #     print("Removing " + temp_folder + "/ folder done.")

    #     return None

    def get_can_signal_description(self) -> Tuple[pd.DataFrame, Dict]:
        """Get available signal information.

        Returns:
            (Tuple[pd.DataFrame]): signal information

        """

        LOGGER.info("Starting to read can signal description.")
        mdf_obj = MDF(self.path)
        mdf_columns = set(list(mdf_obj.channels_db.keys()))

        info_list = []
        unavailable_signals = {}
        for sig in mdf_columns:
            try:
                signal = mdf_obj.get_can_signal(sig)
                signal_information = vars(signal)
                info_list.append(signal_information)
            except MdfException as mdfexception:
                LOGGER.warning(f"The signal {sig} caused this Exception: {mdfexception}")
                unavailable_signals[str(sig)] = mdfexception
            except ValueError as valueerror:
                LOGGER.warning(f"The signal {sig} caused this Exception: {valueerror}")
                unavailable_signals[str(sig)] = valueerror
            except Exception as error:
                LOGGER.warning(f"The signal {sig} caused this Exception: {error}")
                unavailable_signals[str(sig)] = error

        available_signals_df = pd.DataFrame(info_list)

        return (available_signals_df, unavailable_signals)

    def write(self, data) -> None:
        # [ ] TODO implement it
        raise NotImplementedError