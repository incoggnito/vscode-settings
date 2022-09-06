from vallendb import FileHandler
from pathlib import PurePath
from vallendb.utils import trfdb_from_tradb

if __name__ == "__main__":
    wkd = r"C:\Users\ahofer\Desktop\SmartSAD"
    folder = FileHandler("*", wkd=wkd)

    for subfld, files in folder.get_all_subfolders():
        f = FileHandler("*", wkd=wkd, subdir=subfld)
        for fname, fileobj in f.files.items():
            print(fname)
            if fname.endswith("tradb"):
