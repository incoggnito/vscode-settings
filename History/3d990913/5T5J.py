"""Tests for tradbfile"""
import io
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import soundfile as sf
import sqlalchemy as sa
from vallenae.io.datatypes import TraRecord

from vallendb import FileHandler
from vallendb.tradbfile import TradbFile
from vallendb.utils import (
    get_first_last_trai,
    read_global_info,
)

CONFIG = pd.DataFrame.from_dict(
    {
        "All channels same config": ("[-]", False, False),
        "Channel": ("[-]", 1, 2),
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


EXPECTED = {
    "Version": 1,
    "FileStatus": 0,
    "TimeBase": 10000000,
    "BytesPerSample": 2,
    "WriterID": "-",
    "FileID": None,
    "ReferenceID": None,
    "ValidSets": 0,
    "TRAI": 0,
}


@pytest.fixture()
def tradb_handler() -> TradbFile:
    """Create a FileHandler with a single file"""
    tradbfile = FileHandler("Test_old.tradb", subdir=["data", "tests"])
    return tradbfile.current_file


@pytest.fixture()
def tradb_handler_rw(tmp_path: Path) -> TradbFile:
    """Create a FileHandler with a tradb for testing write and read"""
    tradbfile = FileHandler("Test_rw.tradb", subdir=tmp_path)
    with tradbfile(mode="rwc") as tradb:
        tradb.create(config=CONFIG)
    return tradbfile.current_file


def test_create_tradb(tmp_path: Path) -> None:
    filename = "Creation_Test.tradb"
    tradbfile = FileHandler(filename, wkd=tmp_path)
    with tradbfile.current_file(mode="rwc") as tradb:
        tradb.create(config=CONFIG)
    assert tradbfile.exist_file()


def test_rw_no_compression(tradb_handler_rw: TradbFile) -> None:
    """Test reading and writing in a tradb without compressing the data

    Args:
        tmp_path (Path): path to temp directory
    """
    delta_rounded_data = 1e-9
    delta_to_original_data = 1e-6
    tr_mV = 0.00156249975585941  # [ ] TODO implement reading of tr_mV
    # [ ] TODO parametrize this test to check if the deltas are below the above
    #  values for all acquisition settings!
    pretrigger = 0  #: Pretrigger samples
    threshold = 0  #: Threshold amplitude in volts
    samplerate = CONFIG["samplefrequency"]  #: Samplerate in Hz
    samples = CONFIG["blocksize"]  #: Number of samples
    # data_format = 0  #: Data format (0 = uncompressed, 2 = FLAC compression)
    data_complete = []
    data_original = []

    for i in range(1, 5):
        time = (np.ceil(i / 2) - 1) / samplerate  #: Time in seconds
        channel = i % 2 + 1  #: Channel number, 1 and 2 alterning
        param_id = channel + 1  #: Parameter ID of table tr_params for ADC value conversion

        data = np.random.uniform(-1e-3, 1e-3, CONFIG["blocksize"])
        # don't use bigger values otherwise clipping!
        # -32.768, 32.767, CONFIG["Blocksize"]
        # )  #: Transient signal in volts
        trai = int(np.ceil(i / 2))
        with tradb_handler(mode="rw") as tradb:
            tradb.write(
                TraRecord(
                    time,
                    channel,
                    param_id,
                    pretrigger,
                    threshold,
                    samplerate,
                    samples,
                    data,
                    trai,
                ),
                compression=False,
            )
        data_original.append(data)
        data_complete.append(
            np.array(np.int16(np.rint(data * 1e3 / tr_mV)) * 1e-3 * tr_mV, np.float32)
            # not casting to np.int16 doesn't introduce souch an big delta than in
            # the case of compressing the data
        )
    with tradb_handler(mode="rw") as tradb:
        channels = tradb.read()
    for i in range(0, 4):
        if i % 2 == 0:
            # following arrays should be identically: data_complete does
            # the same rounding as vallen for saving
            assert abs(data_complete[i] - channels["CH2"].data.iloc[i // 2]).max() < delta_rounded_data
            # compare the original data with the read data
            assert abs(data_original[i] - channels["CH2"].data.iloc[i // 2]).max() < delta_to_original_data
        else:
            # following arrays should be identically: data_complete does
            # the same rounding as vallen for saving
            assert abs(data_complete[i] - channels["CH1"].data.iloc[i // 2]).max() < delta_rounded_data
            # compare the original data with the read data
            assert abs(data_original[i] - channels["CH1"].data.iloc[i // 2]).max() < delta_to_original_data


def test_rw_with_compression(tradb_handler_rw: TradbFile) -> None:
    """Test reading and writing in a tradb with compressing the data

    Args:
        tmp_path (Path): path to temp directory
    """
    delta_to_original_data = 1e-6
    tr_mV = 0.00156249975585941  # [ ] TODO implement reading of tr_mV
    # [ ] TODO parametrize this test to check if the deltas are below the above
    #  values for all acquisition settings!
    pretrigger = 0  #: Pretrigger samples
    threshold = 0  #: Threshold amplitude in volts
    samplerate = CONFIG.loc[1:, "Samplefrequency"].to_numpy().max()  #: Samplerate in Hz
    samples = CONFIG.loc[1:, "Blocksize"].to_numpy().max()  #: Number of samples
    # data_format = 0  #: Data format (0 = uncompressed, 2 = FLAC compression)
    data_reconstructed = []
    data_original = []

    for i in range(1, 5):
        time = (np.ceil(i / 2) - 1) / samplerate  #: Time in seconds
        channel = i % 2 + 1  #: Channel number, 1 and 2 alterning
        param_id = channel + 1  #: Parameter ID of table tr_params for ADC value conversion

        data = np.random.uniform(-1e-3, 1e-3, samples)
        # don't use bigger values otherwise clipping!
        # -32.768, 32.767, CONFIG["Blocksize"]
        # )  #: Transient signal in volts
        trai = int(np.ceil(i / 2))
        with tradb_handler(mode="rw") as tradb:
            tradb.write(
                TraRecord(
                    time,
                    channel,
                    param_id,
                    pretrigger,
                    threshold,
                    samplerate,
                    samples,
                    data,
                    trai,
                ),
                compression=True,
            )
        data_original.append(data)
        data_int16 = np.int16(np.rint(data * 1e3 / tr_mV))  # important to cast to np.int16, if going on with integer
        # values in float32 type, the compressed data divers heavily
        buffer = io.BytesIO()
        sf.write(buffer, data_int16, 1, format="FLAC")  # samplerate = 1
        data_compressed = buffer.getvalue()
        data_decompressed, _ = sf.read(io.BytesIO(data_compressed), dtype=np.float32)
        factor_libsoundfile = 2 ** 15  # libsoundfile normalizes to +-1
        factor = 1e-3 * tr_mV * factor_libsoundfile
        data_reconstructed.append(np.multiply(data_decompressed, factor, dtype=np.float32))
    with tradb_handler(mode="ro") as tradb:
        channels = tradb.read()
    for i in range(0, 4):
        if i % 2 == 0:
            # following arrays should be identically: data_complete does
            # the same rounding as vallen for saving
            assert abs(data_reconstructed[i] - channels["CH2"].data.iloc[i // 2]).max() == 0
            # compare the original data with the read data
            assert abs(data_original[i] - channels["CH2"].data.iloc[i // 2]).max() < delta_to_original_data
        else:
            # following arrays should be identically: data_complete does
            # the same rounding as vallen for saving
            assert abs(data_reconstructed[i] - channels["CH1"].data.iloc[i // 2]).max() == 0
            # compare the original data with the read data
            assert abs(data_original[i] - channels["CH1"].data.iloc[i // 2]).max() < delta_to_original_data


def test_read_original_format(tradb_handler: TradbFile) -> None:
    """Test read original format
    (just testing if the read is working, because it is only
     wrapping a function from vallen. The read data is
     compared to the writing data in test_rw_with_compression
     and test_rw_no_compression)"""
    with tradb_handler(mode="ro") as tradb:
        data = tradb.read_original_format()


def test_read_global_info(
    tradb_handler: TradbFile,
) -> None:  # [ ] TODO move that to test utils
    """Check global info is correct"""
    assert read_global_info(tradb_handler) == EXPECTED


# def test_read_new_blocksize(tradb_handler: TradbFile) -> None:
#     blocksize = 8912  # [ ] TODO write this test, when the function is implemented
#     df = tradb_handler.read_new_blocksize(blocksize)
#     assert df.data.iloc[0].size == blocksize


def test_set_tr_prams(tradb_handler: TradbFile) -> None:
    """Check that the table tr_params exists"""
    # [ ] TODO@KB,AH Check new attributes in tr_params
    engine = sa.create_engine(f"sqlite:///{tradb_handler.path}")
    insp = sa.inspect(engine)
    assert insp.has_table("tr_params")


def test_get_measurement_duration(tradb_handler: TradbFile) -> None:
    assert tradb_handler.get_measurement_duration() == 0.0262144


def test_get_first_last_trai(tradb_handler: TradbFile) -> None:
    assert get_first_last_trai(tradb_handler) == (1, 1)


def test_read_trai_range() -> None:
    """Test reading of a trai range and handling of overlapping indices of consecutive measurements"""
    f = FileHandler("Test_overlapping_indices.tradb", subdir=["data", "tests"])
    tradbfile = f.current_file
    # [ ] TODO extend the assertion
    # read first measurement
    data = tradbfile.read_trai_range(2, 279)
    assert data.shape == (556, 8)
    # read measurement in the middle
    data = tradbfile.read_trai_range(1393, 1631)
    assert data.shape == (478, 8)
    # read last measurement
    data = tradbfile.read_trai_range(1853, 2035)
    assert data.shape == (366, 8)


def test_read_tr_params(tradb_handler: TradbFile) -> None:

    with tradb_handler(mode="ro") as tradb:
        tr_params = tradb.read_tr_params()
    assert len(tr_params) == 3
    assert tr_params[1]["ADC_µV"] == 0.0
    assert tr_params[1]["TR_mV"] == 0.0
    assert tr_params[2]["ADC_µV"] == 168.33334210069486
    assert tr_params[2]["TR_mV"] == 0.1683333421006949
    assert tr_params[3]["ADC_µV"] == 168.33334210069486
    assert tr_params[3]["TR_mV"] == 0.1683333421006949
