# import os
from pathlib import Path, PurePath

# import numpy as np
import pandas as pd
import pytest

from vallendb import FileHandler
from vallendb.vdbFileHandler.trfdbfile import TrfdbFile

# from typing import Dict


# from vallenae.io import FeatureRecord


# DATA = PurePath(Path(__file__).resolve().parents[1], "data", "tests")

CONFIG = pd.DataFrame.from_dict(
    {
        "All channels same config": ("[-]", False, False),
        "Channel": (1, 2),
        "Channel Description": (
            "[-]",
            "Test Sensor 1, SN: 1234",
            "Test Sensor 2, SN: 9875a",
        ),
        "Measurement mode": ("[-]", "Streaming", "Streaming"),
        "Range": ("[V]", 0.05, 0.05),
        "Preamplifier gain": ("[dB]", 0, 30),
        "Samplefrequency": ("[Hz]", 2_500_000, 1000),
        "Highpass Filter Cutoff Frequency": ("[Hz]", None, 50),
        "Lowpass Filter Cutoff Frequency": ("[Hz]", 1000, None),
        "Filterorder": ("[-]", 8, None),
        "Blocksize": ("[-]", 65536, 1024),
        "Additional Text": (
            "[-]",
            "Additional Infos, like general Messsetup, Temperature, specific data of the measurement",
            "The splitting in channels is for that row a bit meaningless/unwanted.",
        ),
    }
)


@pytest.fixture()
def trfdb_handler() -> TrfdbFile:
    """Create a FileHandler with a single file"""
    trfdbfile = FileHandler("Test_old.trfdb", subdir=["data", "tests"])
    return trfdbfile.current_file


def test_read_trfdb(trfdb_handler: TrfdbFile) -> None:
    """Test the reading of a trfdb

    Args:
        trfdb_handler (TrfdbFile): data/tests/Test_old.trfdb
    """
    with trfdb_handler(mode="ro") as trfdb:
        data = trfdb.read()
    assert data.size == 146030  # [ ] TODO add here a test of the data?


def test_create_trfdb(tmp_path: Path) -> None:
    """Test the creation of a trfdb


    Args:
        tmp_path (Path): path to temp dir
    """
    filename = "Creation_Test.trfdb"
    trfdbfile = FileHandler(filename, wkd=tmp_path)
    with trfdbfile(mode="rwc") as trfdb:
        trfdb.create(CONFIG)
    assert trfdbfile.exist_file()


# def test_write_trfdb() -> None:
#     blocks = 100
#     samples = 65536
#     samplerate = 2.5e6
#     file_path = PurePath(DATA, "Test_write.tradb")
#     data_history = pd.DataFrame(columns=["trai", "data"])
#     data_history.set_index("trai")
#     if os.path.exists(file_path):
#         os.remove(file_path)
#     tradb_file = TradbFile(file_path, CONFIG, mode="rwc", compression=False)
#     for i in range(1, blocks):
#         data = np.random.rand(samples)
#         time_block = float(samples) / samplerate
#         tradb_file.write(
#             TraRecord(
#                 time=(i * time_block),
#                 channel=1,
#                 param_id=3,
#                 pretrigger=0,
#                 threshold=0,
#                 samplerate=samplerate,
#                 samples=samples,
#                 data=data,
#                 trai=2 + i,
#             )
#         )
#         data_history.loc[len(data_history.index)] = {"data": data}
#     data_history["trai"] = data_history.index + 3
#     data_history.set_index("trai", inplace=True)
#     data2 = tradb_file.read()
#     tradb_file.close()
#     # (data_history["data"].sub(data2["CH1"]["data"], axis=0))
#     assert data_history.eq(data2["CH1"].data).any().any()
