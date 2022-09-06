from pathlib import PurePath
from atoolbox import FileHandler
from vallendb.utils import pridb_from_tradb


def generate_pridb(tradbfilepath: PurePath) -> None:

    pridb_from_tradb(tradbfilepath)


if __name__ == "__main__":
    dir_path = PurePath(
        r"C:\Users\KBenkler\Projekt\measurementGUI\data\Measurements\Labortest_Blech\Zusammenschaltung_Piezoscheiben"
    )
    filename = "Stahl_modified_Kalibration_Schlaege_400mV_Range.tradb"
    filepath = dir_path / filename
    f = FileHandler(filename=filepath)
    generate_pridb(f.current_file.path)
