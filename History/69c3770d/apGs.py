from pathlib import PurePath
from vallendb import FileHandler, TradbFile
import pandas as pd
import numpy as np
from vaspy.process import spectrogram, get_freq, fft, fft_mean, spectral_kurtosis
from vaspy.plot import draw_pyqt_spectrogram
import matplotlib.pyplot as plt
import logging


def export_wav(tradbfile: TradbFile) -> None:

    with tradbfile(mode="ro") as tradb:
        timedata = tradb.read()
        for ch, ch_data in timedata.items():
            write_data = np.hstack(ch_data.data)
            f.set_file(f"{filename}_{ch}.wav")
            fs = ch_data.samplerate.unique()[0]
            f.current_file.write(write_data, fs)


if __name__ == "__main__":
    dir_path = PurePath(r"C:\Users\KBenkler\Projekt\measurementGUI\data\Measurements\Beschussversuche_22_04_22")
    filename = "0b_Hohenkorrektur.tradb"
    filepath = dir_path / filename
    f = FileHandler(filename=filepath)
    export_wav(f.current_file)
