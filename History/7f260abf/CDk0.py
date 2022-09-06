import shutil
from pathlib import Path, PurePath

import numpy as np
import pandas as pd
import pytest
import sqlalchemy as sa

from vallendb import FileHandler
from vallendb.pridbfile import PridbFile
from vallendb.utils import (
    get_ae_params,
    get_tr_params,
    pridb_from_tradb,
    read_acq_settings,
    trfdb_from_tradb,
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
#     orient="index",
#     columns=["Unit", "Channel 1", "Channel 2"],
# )

# def test_get_adc_microV() -> None:

# def test_get_ae_params() -> None:

# def test_calc_tr_params() -> None:


def test_hit_from_tra() -> None:
    # [ ] TODO @KB implement that test
    f = FileHandler("sample.tradb", subdir=["data", "tests"])
    with f.current_file(mode="ro") as tradb:
        tr_data = tradb.read_original_format()

    assert False


# def test_connect_db() -> None:
#     # [ ] TODO @AH necessary? is always used

# using a pridb to test utils functions
@pytest.fixture()
def pridb_handler() -> PridbFile:
    """Create a FileHandler with a single file"""
    f = FileHandler("sample.pridb", subdir=["data", "tests"])
    return f.current_file


def test_read_acq_settings(pridb_handler: PridbFile) -> None:
    """Test reading of the acquisition settings

    Args:
        pridb_handler (PridbFile): bigtoolbox\data\tests\sample.pridb
    """
    acq_read = read_acq_settings(pridb_handler.path)
    # workaround for None value entries
    config = CONFIG.where(pd.notnull(CONFIG), 0)
    acq_read = acq_read.where(pd.notnull(acq_read), 0)
    config.index.rename("index", inplace=True)
    assert acq_read.equals(config)


def test_store_acq_settings(tmp_path: Path) -> None:
    """Test the storage of the acquisition settings

    Args:
        pridb_handler (PridbFile): sample.pridb
    """
    f = FileHandler("Test_store_acq.pridb", subdir=tmp_path)
    with f.current_file(mode="rwc") as pridbfile:
        pridbfile.create(CONFIG)
    engine = sa.create_engine(f"sqlite:///{f.fullpath}")
    insp = sa.inspect(engine)
    assert insp.has_table("acq_settings")
    df = pd.read_sql_table("acq_settings", engine, index_col="index")
    df = df.astype(str)  # [ ] TODO remove that workaround (need to have None as "None" as well)
    config = CONFIG.astype(str)  # [ ] TODO remove that workaround
    assert config.equals(df)
    # test set_timebase
    globalinfo = pd.read_sql_table(table_name="ae_globalinfo", con=engine, index_col="Key")
    assert globalinfo.loc["TimeBase", "Value"] == CONFIG.loc[1:, "Samplefrequency"].to_numpy().max()


def test_pridb_from_tradb(tmp_path: Path) -> None:

    # [ ] TODO expand that test
    f = FileHandler("sample.tradb", subdir=["data", "tests"])
    shutil.copy(PurePath(f.fullpath), tmp_path)
    f = FileHandler(filename="sample.tradb", wkd=tmp_path)
    pridb_path = pridb_from_tradb(PurePath(f.fullpath))
    f.set_file(pridb_path)
    assert f.exist_file()


def test_trfdb_from_tradb(tmp_path: Path) -> None:
    # [ ] TODO expand the test
    f = FileHandler("sample.tradb", subdir=["data", "tests"])
    shutil.copy(PurePath(f.fullpath), tmp_path)
    f = FileHandler(filename="sample.tradb", wkd=tmp_path)
    trfdb_path = trfdb_from_tradb(PurePath(f.fullpath))
    f.set_file(trfdb_path)
    assert f.exist_file()


def test_get_ae_params() -> None:
    ae_params = get_ae_params(CONFIG)
    assert False


def test_get_tr_params() -> None:
    tr_params = get_tr_params(CONFIG)
    assert tr_params.shape[0] == CONFIG.shape[0]
    assert tr_params.shape[1] == 5
    assert np.allclose(tr_params["TR_mV"], tr_params["ADC_µV"] / 1000)
