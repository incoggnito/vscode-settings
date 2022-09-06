"""Test all methods according the NVHBrake Database"""

import logging
from typing import Optional

import pandas as pd
import pytest

from atoolbox import NVHBrake

LOGGER = logging.getLogger(__name__)


def check_db_conn() -> Optional[NVHBrake]:
    """Check connection"""
    db = NVHBrake()
    if not db._checkCon():
        db = None
    return db


@pytest.fixture()
def db_conn() -> Optional[NVHBrake]:
    """Create a connection object"""
    db = check_db_conn()
    return db


CON = check_db_conn()
check_db_con = pytest.mark.skipif(CON is None, reason="There is no bmw database connection!")


@check_db_con
def test_writeTable(db_conn: NVHBrake) -> None:
    df = pd.DataFrame([[1, "Hofer", "Andreas"], [2, "Hans", "Peter"]], columns=["ID", "LastName", "FirstName"])
    db_conn.writeTable("tblTest", df)


@check_db_con
def test_showTables(caplog: pytest.LogCaptureFixture, db_conn: NVHBrake) -> None:
    """Test if tables are in db"""
    with caplog.at_level(logging.INFO):
        db_conn.showTables()
    assert "tblTest" in caplog.text


@check_db_con
def test_getTable(db_conn: NVHBrake) -> None:
    df = db_conn.getTable("tblTest")
    assert "Hofer" in df.LastName.values


@check_db_con
def test_updateTable(db_conn: NVHBrake) -> None:
    """Testing to update a table by a dataframe"""
    df = pd.DataFrame(
        [[1, "Johnson", "Andreas"], [2, "Hans", "Peter"], [3, "Hofer", "Andreas"]],
        columns=["ID", "LastName", "FirstName"],
    )
    db_conn.updateTable("tblTest", df, "LastName")
    df = db_conn.getTable("tblTest")
    assert "Hofer" not in df.LastName.values
    assert "Johnson" in df.LastName.values


@check_db_con
def test_insertTable(db_conn: NVHBrake) -> None:
    """Test inserting a new dataframe to a sql table"""
    df = pd.DataFrame([[3, "Hofer", "Andreas"]], columns=["ID", "LastName", "FirstName"])
    db_conn.insertTable("tblTest", df, "ID")
    df = db_conn.getTable("tblTest")
    assert "Hofer" in df.LastName.values


@check_db_con
def test_deleteTable(db_conn: NVHBrake) -> None:
    db_conn.deleteTable("tblTest")
