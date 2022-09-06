import os
from datetime import date

from vallendb import FileHandler


def create_output_folder_structure(measurements: str) -> str:
    print("Available tests:")
    meas = {idx + 1: fld for idx, fld in enumerate(os.listdir(measurements))}
    if not meas:
        idx = int(input("Use 0 to create a new measurement!\n"))
    else:
        print(meas)
        idx = int(input("Select an existing test index or use 0 to create a new!\n"))
    if idx == 0:
        today = date.today()
        material = input("Material: ")
        run = input("Durchlauf: ")
        test = f"{measurements}\\{today}_{material}_{run}"
        os.makedirs(test)
    else:
        test = f"{measurements}\\{meas[idx]}"

    subtest = input("Störung: ")
    v_draht = input("Geschwindigkeit: ")

    fld = os.path.join(test, f"{subtest}_{v_draht}")
    try:
        os.mkdir(fld)
    except FileExistsError:
        pass

    print(f"Created Folders and start a new procedure {subtest}!")
    return os.path.join(fld, f"{subtest}_{v_draht}")


if __name__ == "__main__":
    f = FileHandler(subdir=["data, Measurements"])
    create_output_folder_structure(str(f.fullpath))
