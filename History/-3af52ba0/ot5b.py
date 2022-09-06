from vallendb import FileHandler
from pathlib import PurePath
import numpy as np
import matplotlib.pyplot as plt

from vaspy.process import rolling_average
from vallendb.utils import trfdb_from_tradb

filename = "08_Betriebsmessung"
dir_path = PurePath(r"C:\Users\ahofer\Desktop\INTEUM\00_Messungen_03_05_2022\00_Pos1_VS150M")

sensors = ["Channel 1", "Channel 2"]

# ---- Load TiePie Data
f = FileHandler(
    filename=f"{filename}.tradb",
    wkd=dir_path,
)
feature_selection = [
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
    # "Spectral_fix_Bandwith_10kHz_Analysis",
]
trfdb_from_tradb(
    PurePath(f.fullpath),
    name_extension="_pp",
    feature_selection=feature_selection,
)

f.set_file(f"{filename}_pp.trfdb")
with f.current_file() as trfdb:
    features = trfdb.read()
features.describe()
fig0, ax0 = plt.subplots()
feature = "Crest_Factor"
for ch in features["Channel"].unique():
    smoothed_featuredata = rolling_average(features.loc[features.Channel == ch, feature], 100)
    ax0.plot(
        features.loc[features.Channel == ch, "Time"],
        smoothed_featuredata,
        label=sensors[int(ch) - 1],
    )
    ax0.set_xlabel("Zeit [s]")
    ax0.set_title(feature)
    ax0.grid(True)
    ax0.legend()
fig0.show()
input("Hit return")

if __name__ == "__main__":

    f = FileHandler("*", wkd="")