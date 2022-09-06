from atoolbox import FileHandler


def test_load_single_file() -> None:
    f = FileHandler(filename="panamera_test.mf4", wkd="git_root", subdir=["data", "MF4"])
    f.read()
    ...
