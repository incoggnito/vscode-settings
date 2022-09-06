"""Test mdf4files."""
from atoolbox import FileHandler


def test_load_mf4file() -> None:
    """Test the mdf4file handling"""
    f = FileHandler(
        filename="SES123_992_C4S-20201119-095430.mf4",  # "SES123_992_C4S-20201119-095102.mf4",
        wkd=r"C:\Users\KBenkler\Documents\Forschungsprojekte\00_Aktiv\Panamera\Messdaten\mf4_files",
    )
    valid_meta, invalid_meta = f.current_file.get_can_signal_description()
    df = f.current_file.read()
    f.set_file("Columns_mf4_file.txt")
    f.current_file.write(content=df.columns, linewise=True)
    assert False


# def test_append_data(tmp_path: Path) -> None:
#     """Test appending data to file"""
#     f = FileHandler("test.txt", tmp_path)
#     data = "test"
#     f.current_file.write(data)
#     f.current_file.write(data, mode="a")
#     expected = data + data
#     assert f.current_file.read() == expected
