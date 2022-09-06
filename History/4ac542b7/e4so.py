"""Test Db FileHandler."""

from datetime import datetime
import pandas as pd
import pytest

from atoolbox import FileHandler
from atoolbox.FileHandler.dbfile import DbFile


@pytest.fixture()
def db_handler() -> DbFile:
    """Create a FileHandler with a db file"""
    f = FileHandler("Test.db", subdir=["data", "Test_Folder", "DB_Files"])
    return f.current_file


def test_get_tables(db_handler: DbFile) -> None:
    """Test get tables in db"""
    tables = ["1234%", "Tabelle1", "Taebelleß"]
    db_handler.get_tables()
    assert db_handler.tables == tables


def test_get_views(db_handler: DbFile) -> None:
    """Test get views in db"""
    views = ["t1789$", "view1", "viewß$"]
    db_handler.get_views()
    assert db_handler.views == views


def test_read_day(db_handler: DbFile) -> None:
    """Test the function read day

    Args:
        db_handler (DbFile):Test.db
    """
    day1 = db_handler.read_day(table="Tabelle1", day=datetime(2021, 8, 4), time_col="Time")
    day2 = db_handler.read_day(table="Tabelle1", day=datetime(2021, 8, 5), time_col="Time")
    day3 = db_handler.read_day(table="Tabelle1", day=datetime(2021, 8, 6), time_col="Time")
    assert day1.shape[0] == 44
    assert day2.shape[0] == 87
    assert day3.shape[0] == 70


def test_read_time_section(db_handler: DbFile) -> None:
    """Test the function read time section

    Args:
        db_handler (DbFile):Test.db
    """
    section_data = db_handler.read_time_section(
        table="Tabelle1",
        startpoint=datetime(2021, 8, 5, 10, 55, 15),
        endpoint=datetime(2021, 8, 5, 10, 57),
        time_col="Time",
    )
    assert section_data.shape[0] == 11
    assert section_data.index[0] == pd.Timestamp("2021-08-05 10:55:15.671248")
    assert section_data.index[-1] == pd.Timestamp("2021-08-05 10:56:01.530630")


def test_read_time_section_w_initial(db_handler: DbFile) -> None:
    """Test the function read time section with the option initial value

    Args:
        db_handler (DbFile):Test.db
    """
    section_data = db_handler.read_time_section(
        table="Tabelle1",
        startpoint=datetime(2021, 8, 5, 10, 55, 15),
        endpoint=datetime(2021, 8, 5, 10, 57),
        time_col="Time",
        initial_value=True,
    )
    assert section_data.shape[0] == 12
    assert section_data.index[0] == pd.Timestamp("2021-08-05 10:55:14.389894")
    assert section_data.index[-1] == pd.Timestamp("2021-08-05 10:56:01.530630")
