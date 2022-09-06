from vallendb import FileHandler
import pandas as pd
import sqlite3
from datetime import datetime

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
    df['Time'] = [datetime.fromtimestamp(d) for d in df['Time']]
    df = df.sort_values(by="Time")
    df_left = df[df.Channel == 1]
    df_left = df_left.reset_index(drop=True)
    df_right = df[df.Channel == 2]
    df_right = df_right.reset_index(drop=True)
    df = df_left.join(df_right, how = "left", lsuffix="_1", rsuffix="_2")
    conn = sqlite3.connect("20_05_04-all_features_db_pre_learning.sql")
    df.to_sql("measurement", conn, if_exists="append")


