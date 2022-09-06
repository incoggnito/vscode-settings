from vallendb import FileHandler
import pandas as pd
import sqlite3

if __name__ == "__main__":
    wkd = r"C:\Users\ahofer\Desktop\SmartSAD"
    folder = FileHandler("*", wkd=wkd)
    df_List = []
    for subfld, files in folder.get_all_subfolders():
        f = FileHandler("*", wkd=wkd, subdir=subfld)
        for fname, fileobj in f.files.items():
            if fname.endswith("pp.trfdb"):
                print(fname)
                with fileobj() as trfsb:
                    df_List.append(trfsb.read())

    df = pd.concat(df_List)

    try:
        sqlite3.connect("20_05_04-all_features_db_pre_learning.sql")
        pd.to_sql()

