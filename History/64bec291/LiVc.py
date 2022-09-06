import sqlite3
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
    conn = sqlite3.connect("20_05_04-all_features_db_pre_learning.db")
    df.to_sql("measurement", conn)
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

if __name__ == "__main__":
    wkd = r"C:\Users\ahofer\Desktop\SmartSAD\Durchlauf_9_05_auf_8_3"
    create_trfdb(wkd)
    df = merge_trfdb(wkd)
    