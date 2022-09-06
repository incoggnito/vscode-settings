"""Test FileHandler."""

from pathlib import Path

from atoolbox import FileHandler


def test_load_json(tmp_path: Path) -> None:
    """Test the json handling"""
    j = FileHandler("test.pkl", tmp_path)
    t1_dict = {"test": 1}
    j.write(t1_dict)
    assert j.read() == t1_dict


def test_multi_load_json(tmp_path: Path) -> None:
    """Test the json handling"""
    j = FileHandler("test.pkl", tmp_path)
    j2 = FileHandler("test2.pkl", tmp_path)
    t1_dict = {"test": 1}
    j.write(t1_dict)
    j2.write(t1_dict)
    test = j.read()
    test2 = j2.read()
    assert test == test2 == t1_dict
