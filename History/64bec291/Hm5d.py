import vallendb
from vallendb import FileHandler
from pathlib import PurePath
from vallendb.utils import trfdb_from_tradb

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

if __name__ == "__main__":
    wkd = r"C:\Users\ahofer\Desktop\INTEUM\00_Messungen_03_05_2022"
    folder = FileHandler("*", wkd=wkd)

    for subfld, files in folder.get_all_subfolders():
        f = FileHandler("*", wkd=wkd, subdir=subfld)
        for fname, fileobj in f.files.items():
            print(fname)
            if fname.endswith("tradb"):
                trfdb_from_tradb(
                    PurePath(fileobj.path),
                    name_extension="_pp",
                    feature_selection=FEATURES,
                )