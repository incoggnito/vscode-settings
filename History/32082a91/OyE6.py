from vallendb import FileHandler
import pandas as pd
from functools import reduce

if __name__ == "__main__":
    wkd = r"C:\Users\ahofer\Desktop\SmartSAD"
    folder = FileHandler("*", wkd=wkd)
    df_List = []
    for subfld, files in folder.get_all_subfolders():
        f = FileHandler("*", wkd=wkd, subdir=subfld)
        for fname, fileobj in f.files.items():
            if fname.endswith("pp.trfdb"):
                print(fname)
                with fileobj as trfsb:
                    df_List.append(trfsb.read())

    df = reduce(lambda x, y: pd.merge(x, y, on = 'Date'), df_List)
