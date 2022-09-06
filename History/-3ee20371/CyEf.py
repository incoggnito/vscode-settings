from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import sqlalchemy as sa

from vallendb import FileHandler, PridbFile

# [ ] TODO https://cloud.amitronics.net/f/160886

# hit bases measurement always with the highest available samplefrequency

CONFIG_KEYS = [
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
    "Duration Discrimination Time",
    "Status Interval",
    "Threshold",
    "Transient data acquisition",
    "Pretrigger samples",
    "Post duration samples",
    "Additional Text",
]
CONFIG_UNITS = {
    "All channels same config": "[-]",
    "Channel": "[-]",
    "Channel Description": "[-]",
    "Measurement mode": "[-]",
    "Range": "[V]",
    "Preamplifier gain": "[dB]",
    "Samplefrequency": "[Hz]",
    "Highpass Filter Cutoff Frequency": "[Hz]",
    "Lowpass Filter Cutoff Frequency": "[Hz]",
    "Filterorder": "[-]",
    "Blocksize": "[-]",
    "Duration Discrimination Time": "[micros]",
    "Status Interval": "[ms]",
    "Threshold": "[microV]",
    "Transient data acquisition": "[-]",
    "Pretrigger samples": "[-]",
    "Post duration samples": "[-]",
    "Additional Text": "[-]",
}
# [ ] Review @LB it is possible to use different measurement modes for different channels?
# [ ] Review @LB, maybe it it possible to record one channel with different modes at the same time -> output data mapped to different data channels
CONFIG_HEAD_1 = {  # [ ] TODO take this as input parameter to create tradb?
    "All channels same config": True,
    "Channel": 1,
    "Channel Description": "Test Sensor 1, some specs (Description, Location, ...)",
    "Measurement mode": "Streaming",
}
CONFIG_HEAD_2 = {
    "All channels same config": True,
    "Channel": 2,
    "Channel Description": "Test Sensor 2, with some other specs (Description, Location, ...)",
    "Measurement mode": "Streaming",
}

CONFIG_ALL_CH = {
    "Range": 0.05,
    "Preamplifier gain": 0,
    "Samplefrequency": 2500000,
    "Highpass Filter Cutoff Frequency": 0,
    "Lowpass Filter Cutoff Frequency": 1000,
    "Filterorder": 8,
    "Blocksize": 65536,
}

CONFIG_CH1 = {**CONFIG_HEAD_1, **CONFIG_ALL_CH}
CONFIG_CH2 = {**CONFIG_HEAD_2, **CONFIG_ALL_CH}

CONFIG = pd.DataFrame(
    [
        CONFIG_UNITS,
        CONFIG_CH1,
        CONFIG_CH2,
    ],
    columns=CONFIG_KEYS,
)


# pridbfile._write_guid dont need to be tested (executed at creation of pridb)


@pytest.fixture()
def pridb_handler() -> PridbFile:
    """Create a FileHandler with a test pridb file"""
    f = FileHandler("Test.pridb", subdir=["data", "tests"])
    return f.current_file


@pytest.fixture()
def pridb_handler_old() -> PridbFile:
    """Create a FileHandler with a test pridb file"""
    f = FileHandler("Test_old.pridb", subdir=["data", "tests"])
    return f.current_file


def test_create_pridb(tmp_path: Path) -> None:
    """Tests the creation of a pridb

    Args:
        tmp_path (Path): path to the tempory directory
    """
    filename = "Creation_Test.pridb"
    f = FileHandler(filename, wkd=tmp_path)
    with f.current_file(mode="rwc") as pridb:
        pridb.create(config=CONFIG)
    assert f.exist_file()


def test_read(pridb_handler_old: PridbFile) -> None:
    with pridb_handler_old(mode="ro") as pridb:
        _ = pridb.read()
    assert pridb.channels["CH1"].shape == (422, 11)
    assert pridb.channels["CH2"].shape == (422, 11)
    assert (np.array(pridb.channels["CH1"].trai) == np.arange(2, 424)).all()
    assert (np.array(pridb.channels["CH2"].trai) == np.arange(2, 424)).all()
    # [ ] TODO get the following comparision to work (relabel columns, drop Nans, same units as Lukas..)
    # engine = sa.create_engine(f"sqlite:///{pridb_handler.path}")
    # data = pd.read_sql_table(table_name="ae_data", con=engine, index_col="SetID")
    # channels_ref = [x.dropna(axis=1, how="all") for name, x in data.groupby("Chan")]
    # for i, ch in enumerate(channels_ref):
    #     ch.drop("Status", axis=1, inplace=True)
    #     ch.Time = ch.Time * 1e-6  # [ ] TODO read the sample frequency? 1/fs = 1e-6
    #     ch.index.rename("set_id", inplace=True)
    #     assert ch == channels[list(channels.keys())[i]]
    # [ ] TODO test also the data?


def test_read_markers(pridb_handler: PridbFile) -> None:
    """Test the read of markers

    Args:
        pridb_handler (PridbFile): Test.pridb handler
    """
    with pridb_handler(mode="ro") as pridb:
        markers = pridb.read_markers()
    engine = sa.create_engine(f"sqlite:///{pridb_handler.path}")
    data = pd.DataFrame(pd.read_sql_table(table_name="ae_markers", con=engine, index_col="SetID"))
    assert (data.Data == markers.data).all()
    assert (data.Number.dropna() == markers.number.dropna()).all()


def test_parse_markers(pridb_handler: PridbFile) -> None:
    """Test the parsing of the markers

    Args:
        pridb_handler (PridbFile): Test.pridb handler
    """
    with pridb_handler(mode="ro") as pridb:
        parsed_markers = pridb.parse_markers()
    expected_cols = [
        "Start TRAI",
        "Stop TRAI",
        "Start abs.",
        "End abs.",
        "Start rel. [s]",
        "End rel. [s]",
        "Start SetID",
        "Stop SetID",
        "Measurement duration abs. [s]",
    ]
    expected = pd.DataFrame(
        [
            [
                2,
                279,
                "2021-08-04 13:23:16.176903",
                "2021-08-04 13:23:34.437932",
                0.065536,
                36.634623,
                4,
                559,
                18.261029,
            ],
            [
                279,
                1049,
                "2021-08-04 13:27:40.542652",
                "2021-08-04 13:28:31.163684",
                36.700159,
                138.018816,
                565,
                2106,
                50.621032,
            ],
            [
                1050,
                1393,
                "2021-08-04 13:28:42.227517",
                "2021-08-04 13:29:04.808170",
                138.084352,
                183.435264,
                2112,
                2799,
                22.580653,
            ],
            [
                1393,
                1631,
                "2021-08-04 13:29:15.662822",
                "2021-08-04 13:29:31.382792",
                183.500800,
                215.089151,
                2805,
                3282,
                15.719970,
            ],
            [
                1631,
                1853,
                "2021-08-04 13:29:49.800727",
                "2021-08-04 13:30:04.466477",
                215.154687,
                244.645888,
                3288,
                3733,
                14.665750,
            ],
            [
                1853,
                2035,
                "2021-08-04 13:30:22.053676",
                "2021-08-04 13:30:34.077520",
                244.711424,
                268.959744,
                3739,
                4104,
                12.023844,
            ],
            [
                2035,
                2677,
                "2021-08-04 13:42:12.262592",
                "2021-08-04 13:42:54.437037",
                269.025280,
                353.501183,
                4110,
                5394,
                42.174445,
            ],
            [
                2677,
                3113,
                "2021-08-04 13:48:24.808907",
                "2021-08-04 13:48:53.534297",
                353.566719,
                411.107328,
                5400,
                6273,
                28.725390,
            ],
            [
                3114,
                3556,
                "2021-08-04 13:55:15.168079",
                "2021-08-04 13:55:44.231249",
                411.172864,
                469.434368,
                6279,
                7163,
                29.063170,
            ],
            [
                3556,
                3718,
                "2021-08-04 13:57:39.592264",
                "2021-08-04 13:57:50.341730",
                469.499904,
                491.126784,
                7169,
                7494,
                10.749466,
            ],
            [
                3718,
                4024,
                "2021-08-04 14:01:57.506050",
                "2021-08-04 14:02:17.663100",
                491.192320,
                531.693568,
                7500,
                8113,
                20.157050,
            ],
            [
                4024,
                4444,
                "2021-08-04 14:09:28.918776",
                "2021-08-04 14:09:56.566437",
                531.759104,
                587.202560,
                8119,
                8960,
                27.647661,
            ],
            [
                4444,
                5486,
                "2021-08-04 14:12:34.225757",
                "2021-08-04 14:13:42.664277",
                587.268095,
                724.238336,
                8966,
                11051,
                68.438520,
            ],
            [
                5486,
                5838,
                "2021-08-04 14:28:14.462411",
                "2021-08-04 14:28:37.667630",
                724.303872,
                770.834432,
                11057,
                11762,
                23.205219,
            ],
        ],
        columns=expected_cols,
    )
    comparsion = parsed_markers == expected
    assert comparsion["Start abs."].all()
    assert comparsion["End abs."].all()
    assert comparsion["Start rel. [s]"].all()
    assert comparsion["End rel. [s]"].all()
    assert comparsion["Start SetID"].all()
    assert comparsion["Stop SetID"].all()
    # assert np.isclose(
    #     parsed_markers["Measurement duration rel. [s]"],
    #     expected["Measurement duration rel. [s]"],
    # ).all()
    assert np.isclose(
        parsed_markers["Measurement duration abs. [s]"],
        expected["Measurement duration abs. [s]"],
    ).all()


def test_setid_to_trai(pridb_handler: PridbFile) -> None:
    """Test the setid_to_trai

    Args:
        pridb_handler (PridbFile): Test.pridb handler
    """
    with pridb_handler(mode="ro") as pridb:
        trai1 = pridb.setid_to_trai(1)
        trai2 = pridb.setid_to_trai(4)
        trai3 = pridb.setid_to_trai(11762)
        trai4 = pridb.setid_to_trai(11764)

    assert trai1 is None
    assert trai2 == 2
    assert trai3 == 5838
    assert trai4 is None


@pytest.mark.parametrize("measurement", range(0, 13))
def test_read_measurement(pridb_handler: PridbFile, measurement: int) -> None:

    timefactor = 1e-6
    adc_microV = 1.56249975585941 * timefactor  # [ ] TODO why is here the timefactor needed?
    adc_te = 0.000244140548706073
    # adc_ss = 0.00156249975585941 # needed, when testing signal strength aswell
    block_factor = 0.0065536  # [ ] TODO check that factor (blocksize/fs ?)
    with pridb_handler(mode="ro") as pridb:
        meas_data = pridb.read_measurement(measurement)
    if meas_data["CH1"].index[0] < meas_data["CH2"].index[0]:
        setid_start = meas_data["CH1"].index[0]
    else:
        setid_start = meas_data["CH2"].index[0]

    if meas_data["CH1"].index[-1] > meas_data["CH2"].index[-1]:
        setid_stop = meas_data["CH1"].index[-1]
    else:
        setid_stop = meas_data["CH2"].index[-1]
    engine = sa.create_engine(f"sqlite:///{pridb_handler.path}")
    data = pd.DataFrame(pd.read_sql_table(table_name="ae_data", con=engine, index_col="SetID"))
    data = data.iloc[setid_start - 1 : setid_stop]  # [ ] TODO check, why this -1 is needed
    data = data.dropna(subset=["Chan"]).dropna(axis=1)
    reference_data = {"CH%d" % name: x for name, x in data.groupby("Chan")}
    # assert channel 1
    assert np.isclose(meas_data["CH1"].time, reference_data["CH1"].Time * timefactor).all()
    assert np.isclose(meas_data["CH1"].amplitude, reference_data["CH1"].Amp * adc_microV).all()
    assert np.isclose(meas_data["CH1"].energy, reference_data["CH1"].Eny * adc_te).all()
    assert np.isclose(meas_data["CH1"].rms, reference_data["CH1"].RMS * block_factor * adc_microV).all()
    # assert channel 2
    assert np.isclose(meas_data["CH2"].time, reference_data["CH2"].Time * timefactor).all()
    assert np.isclose(meas_data["CH2"].amplitude, reference_data["CH2"].Amp * adc_microV).all()
    assert np.isclose(meas_data["CH2"].energy, reference_data["CH2"].Eny * adc_te).all()
    assert np.isclose(meas_data["CH2"].rms, reference_data["CH2"].RMS * block_factor * adc_microV).all()


def test_read_ae_params(pridb_handler: PridbFile) -> None:

    with pridb_handler(mode="ro") as pridb:
        pridb.read_ae_params()
    assert len(pridb_handler.ae_params) == 3
    assert pridb_handler.ae_params[1]["ADC_µV"] == 0.0
    assert pridb_handler.ae_params[1]["ADC_TE"] == 0.0
    assert pridb_handler.ae_params[1]["ADC_SS"] == 0.0
    assert pridb_handler.ae_params[2]["ADC_µV"] == 1.56249975585941
    assert pridb_handler.ae_params[2]["ADC_TE"] == 0.000244140548706073
    assert pridb_handler.ae_params[2]["ADC_SS"] == 0.00156249975585941
    assert pridb_handler.ae_params[3]["ADC_µV"] == 1.56249975585941
    assert pridb_handler.ae_params[3]["ADC_TE"] == 0.000244140548706073
    assert pridb_handler.ae_params[3]["ADC_SS"] == 0.00156249975585941


# def test_duration_since_start() -> None:

# def test_insert_marker() -> None:

# def test_write_start_markers() -> None:

# def test_write_label() -> None:

# def test_set_all_sets_valid() -> None:

# def test_write() -> None:

# def test_write_ae_params() -> None:

# def test_write_stop_marker() -> None:
