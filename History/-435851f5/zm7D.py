from pathlib import PurePath
from vallendb import FileHandler, TradbFile
import numpy as np

def export_wav(tradbfile: TradbFile) -> None:

    with tradbfile(mode="ro") as tradb:
        timedata = tradb.read()
        for ch, ch_data in timedata.items():
            write_data = np.hstack(ch_data.data)
            f.set_file(f"{filename}_{ch}.wav")
            fs = ch_data.samplerate.unique()[0]
            f.current_file.write(write_data, fs)

if __name__ == "__main__":

    wkd = r"C:\Users\ahofer\Desktop\SmartSAD\Durchlauf_9_05_auf_8_3"
    folder = FileHandler("*", wkd=wkd)
    for fname, fileobj in folder.files.items():
        if fname.endswith(".tradb"):
            print(fname)
            with fileobj() as tradb:
                export_wav(tradb.path)

    # dir_path = PurePath(
    #     r"C:\Users\ahofer\Desktop\INTEUM\00_Messungen_03_05_2022\00_Pos1_VS150M"
    # )
    # filename = "03_Betrieb4.tradb"
    # filepath = dir_path / filename
    # f = FileHandler(filename=filepath)
    # export_wav(f.current_file)

