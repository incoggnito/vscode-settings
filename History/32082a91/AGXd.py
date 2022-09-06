from vallendb import FileHandler

if __name__ == "__main__":
    wkd = r"C:\Users\ahofer\Desktop\SmartSAD"
    folder = FileHandler("*", wkd=wkd)
    l = []
    for subfld, files in folder.get_all_subfolders():
        f = FileHandler("*", wkd=wkd, subdir=subfld)
        for fname, fileobj in f.files.items():
            if fname.endswith("pp.trfdb"):
                print(fname)
                with fileobj as trfsb:
                    l.append(trfsb.read())

    pandas
