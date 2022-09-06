
import sqlite3

from matplotlib.pyplot import new_figure_manager
from vallendb import FileHandler
from pathlib import PurePath
from vallendb.utils import trfdb_from_tradb
from datetime import datetime

import pandas  as pd

FEATURES = [
        "Energy_Pridb",
        "Signal_Strength",
        "Mean",
        "ATO_Hinkley",
        "ATO_AIC",
        "ATO_ER",
        "ATO_MER",
        "Hit_Peak",
        "Hit_Risetime",
        "Hit_RA_Value",
        "Hit_ZCR",
        "Hit_Energy",
        "Power_Mean",
        "RMS",
        "Peak_Amplitude",
        "Crest_Factor",
        "K_Factor",
        "Impulse_Factor",
        "Margin_Factor",
        "Shape_Factor",
        "Clearance_Factor",
        "Zero_Crossing_Rate",
        "Spectral_Peak",
        "Spectral_Centroid",
        "Spectral_Spread",
        "HFC",
        "Spectral_Rolloff",
        "Spectral_Flatness",
        "Percentile",
        "STD",
        "Skewness",
        "Kurtosis",
        "FFT_Mean",
        "Envelope_Peak",
        "Envelope_Centroid",
        "Envelope_Spread",
        "Envelope_HFC",
        "Envelope_Rolloff",
        "Envelope_Mean",
    ]


def merge_trfdb(wkd:str) -> pd.DataFrame:
    folder = FileHandler("*", wkd=wkd)
    df_List = []

    for fname, fileobj in folder.files.items():
        if fname.endswith("pp.trfdb"):
            print(fname)
            with fileobj() as trfdb:
                df = trfdb.read()
                df["TRAI"] = df.index
                df["fileid"]=int(fname.split("_")[0])
                df_List.append(df)

    df = pd.concat(df_List)
    df['Time'] = [datetime.fromtimestamp(d) for d in df['Time']]
    df = df.sort_values(by="Time")
    df_left = df[df.Channel == 1]
    df_left = df_left.reset_index(drop=True)
    df_right = df[df.Channel == 2]
    df_right = df_right.reset_index(drop=True)
    df = df_left.join(df_right, how = "left", lsuffix="_1", rsuffix="_2")
    df = df.drop(["Channel_1", "Time rel. [s]_1", "Channel_2", "Time rel. [s]_2"], axis=1)
    # conn = sqlite3.connect("20_05_04-all_features_db_pre_learning.db")
    # df.to_sql("measurement", conn)
    return df

def create_trfdb(wkd:str):
    folder = FileHandler("*", wkd=wkd)
    counter = 0
    for fname, fileobj in folder.files.items():
        if fname.endswith(".tradb"):
            print(fname)
            with fileobj() as file:
                last = file.get_last_time_trai()
                counter = counter + last[1]
            trfdb_from_tradb(
                PurePath(fileobj.path),
                name_extension="_pp",
                feature_selection=FEATURES,
            )

def merge_new_to_old_features_on_time(old: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    old = create_time_index(old, "timestamp_sent_vam_data")
    new = create_time_index(new, "Time_1")

    return old.join(new, how="left")

def merge_new_to_old_features_on_index(old: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    new = new.set_index(new["TRAI_2"], drop=True)
    old = old.set_index(old["trai_ch1"], drop=True)
    return old.join(new, how="left")

def create_time_index(df:pd.DataFrame, col = "timestamp_sent_vam_data"):
    df["Time"] = pd.to_datetime(df[col])
    df = df.sort_values(by="Time")
    return df.set_index("Time", drop=True)

def get_old_features(wkd: str):
    conn = sqlite3.connect(f"{wkd}/ml_database.db")
    df = pd.read_sql("SELECT * FROM measurement", conn)
    df = df.drop([str(i) for i in range(8)] + ["index"], axis=1)
    return df

if __name__ == "__main__":
    wkd = "C:/Users/ahofer/Desktop/Test"
    # create_trfdb(wkd)
    new_features = merge_trfdb(wkd)
    old_features = get_old_features(wkd)
    df = merge_new_to_old_features_on_index(old_features, new_features)
    #df = merge_new_to_old_features_on_time(old_features ,new_features)
    # TODO sort
    conn = sqlite3.connect(f"{wkd}/master.db")
    df.to_sql("measurement", conn, if_exists="replace")