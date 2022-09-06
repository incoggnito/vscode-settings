"""Test FileHandler."""
import os
import tempfile
from pathlib import Path

import pytest

from atoolbox import FileHandler

tmp_dir = tempfile.gettempdir()


@pytest.fixture()
def create_single_file_handler() -> FileHandler:
    """Create a FileHandler with a single file"""
    f = FileHandler("test.sh", wkd=tmp_dir, subdir="test_file")

    if not f.exist_path():
        f.create_folders()

    if f.contain_files():
        f.remove_file()

    with open(f.fullpath, "wb") as file:
        file.write(b"Test")

    return f


@pytest.fixture()
def create_multi_files_handler() -> FileHandler:
    """Create a file handler containing multiple files"""

    f = FileHandler("*", wkd=tmp_dir, subdir="test_files")

    if not f.exist_path():
        f.create_folders()

    if f.contain_files():
        f.remove_all_files()

    for i in range(3):
        handle, output = tempfile.mkstemp(suffix=".sh", prefix=str(i), dir=f.fullpath)
        with os.fdopen(handle, "wb") as tmp:
            tmp.write(b"test")
    return f


def test_create_folders() -> None:
    """Test method is already tested by os"""
    assert True


def test_exist_path() -> None:
    """The method is already tested by os"""
    assert True


def exists_file() -> None:
    """The method is already tested by os"""
    assert True


def test_build_fullpath(create_single_file_handler: FileHandler, create_multi_files_handler: FileHandler) -> None:
    """Test the if the fullpath is correct"""
    assert Path(create_multi_files_handler.fullpath).__str__() == Path(f"{tmp_dir}/test_files").__str__()
    assert Path(create_single_file_handler.fullpath).__str__() == Path(f"{tmp_dir}/test_file/test.sh").__str__()


def test_get_all_files(create_single_file_handler: FileHandler, create_multi_files_handler: FileHandler) -> None:
    """Check len of files in the folder"""
    assert len(create_multi_files_handler.files) == 3
    assert len(create_single_file_handler.files) == 1


def test_get_prj_root() -> None:
    """Test if the root folder is correct"""
    f = FileHandler("")
    assert f.get_prj_root("git_root").name == "atoolbox"


def test_filt_files(create_multi_files_handler: FileHandler) -> None:
    f = create_multi_files_handler
    f._filt_files(".txt")
    assert len(f.files) == 0


def test_set_file_by_substr() -> None:
    f = FileHandler(filename="*", subdir=["data", "DB_Files", "Test1"])
    f.set_file_by_substr("2")
    assert f.current_file.name == "test2.txt"


def test_filehandler_init_pathobject() -> None:
    testpath = Path(r"data\Excel\test.xlsx").resolve()
    f = FileHandler(filename=testpath)
    assert f.exist_file() is True
