"""Contains some stuff for file handling.

Created on Thu Oct 22 07:50:37 2020

@author: Andreas Hofer
"""

import logging
import os
import shutil
from pathlib import Path, PurePath
from typing import Any, List, Tuple, Union, Dict

from atoolbox.FileHandler.utils import (
    BaseFile,
    BaseFiles,
    FileTypeError,
    get_project_root,
)

LOGGER = logging.getLogger(__name__)


class FileHandler:
    """Easier file management in python."""

    def __init__(
        self,
        filename: Union[os.PathLike, str] = "*",
        wkd: Union["os.PathLike[str]", str] = "git_root",
        subdir: Union[str, List[str]] = "",
        filt_ftype: str = "",
    ):
        """Initialize the current working directory.

        Args:
            filename Union[os.PathLike, str]: The filename (with file extension!) or the complete path to the file
            wkd (os.PathLike, str): The current git root folder.
            subdir (str, List(str)): Subfolder elements.
            filt_ftype (str): Filter files on specific ending.
        """

        self.parse_filename(filename, wkd, subdir)

        self.files = BaseFiles()
        if self.exist_path():
            self.get_all_files()
        else:
            LOGGER.exception(
                "Directory does not exists." "Please use FileHandler.create_folders() to create them.",
            )
        self.set_file(self.active_filename)
        self._filt_files(filt_ftype=filt_ftype)

    def parse_filename(
        self, filename: Union[os.PathLike, str], wkd: Union["os.PathLike[str]", str], subdir: Union[str, List[str]]
    ) -> None:
        """parse the filename, wkd and subdir

        Args:
            filename (Union[os.PathLike, str]): The filename (with file extension!) or the complete path to the file
            wkd (os.PathLike, str): The current git root folder.
            subdir (str, List(str)): Subfolder elements.
        """
        if os.path.exists(filename):
            LOGGER.info("The filename is a complete path! Entries in subdir are removed!")
            self._set_active_file(os.path.basename(filename))
            self.wkd = PurePath(os.path.dirname(filename))
            self.subdir = ""
            self.dir = os.path.dirname(filename)
            self.fullpath = PurePath(filename)
        else:
            if isinstance(filename, str):
                filename = filename.strip()
            if isinstance(wkd, str):
                wkd = wkd.strip()
            if isinstance(subdir, str):
                subdir = subdir.strip()
            # [ ] TODO don't be case sensitiv for the suffixes? e.g.: accept .JPG and .jpg
            self._set_active_file(os.path.basename(filename))
            self.wkd = self.get_prj_root(wkd)
            self.subdir = self.set_subfolder(subdir)
            self.dir = self.set_dir(self.subdir)
            self.fullpath = PurePath(self.dir, filename)

    def set_file_by_substr(self, substr: str) -> None:
        """Set the current file by a substring of a key"""
        for fname, _ in self.files.items():
            if substr in fname:
                self.set_file(fname)
                break

    def _set_active_file(self, filename: str) -> None:
        """Set current file"""
        if filename in ["*", None]:
            self.active_filename = ""
        else:
            self.active_filename = filename

    def _filt_files(self, filt_ftype: str) -> None:
        """Filter all files by given filetype"""
        if filt_ftype:
            self.files = BaseFiles({name: fobj for name, fobj in self.files.items() if name.endswith(filt_ftype)})

    # def _filt_names(self, filt_name: str) -> None:
    #     """Filter all files by given name""" # [ ] TODO @KB
    #     if filt_name:
    #         self.files = [forf in self.files if filt_name in f.name]

    def get_prj_root(self, wkd: Union[str, "os.PathLike[str]"] = "") -> PurePath:
        """Get current project src root directory"""
        root = PurePath(os.getcwd())
        if os.path.dirname(self.active_filename):
            prj = PurePath(os.path.dirname(self.active_filename))
        elif wkd in ["git_root", None, ""]:
            prj = get_project_root()
        elif Path(wkd).is_dir():
            prj = PurePath(wkd)
        else:
            LOGGER.warning("Wkd not valid!")
            prj = root

        return prj

    def __repr__(self) -> str:
        """Describe your self"""
        return f"FileHandler({self.fullpath})"

    def _try_touch(self) -> None:
        """Creates a new emptry file if not exists"""
        if not self.exist_file():
            answer = input("File does not exist! Create empty? (Y/n)")
            if answer.lower() == "y":
                Path(self.fullpath).touch()

    def read(self, *args: Tuple, **kwargs: Dict) -> Any:
        """Method to call a read operation on the active file"""
        if self.current_file:
            return self.current_file.read(*args, **kwargs)
        return None

    def read_all(self, *args: Tuple, **kwargs: Dict) -> Any:
        """Method to read all files"""
        self.files.read(*args, **kwargs)

    def write(self, *args: Tuple, **kwargs: Dict) -> Any:
        """Method to call a write operation on the active file"""
        if self.current_file:
            return self.current_file.write(*args, **kwargs)
        return None

    def write_all(self, *args: Tuple, **kwargs: Dict) -> Any:
        """Method to write all files"""
        self.files.write(*args, **kwargs)

    @staticmethod
    def set_subfolder(subdir: Union[str, list]) -> str:
        """Set the current sub folder"""

        if isinstance(subdir, list):
            subdir = os.path.join(*subdir)

        return str(subdir)

    def set_file(self, new_fname: str) -> None:
        """Reset the current file object"""
        self._set_active_file(new_fname)
        self.set_fullpath()
        self.current_file = self.get_file(PurePath(self.fullpath))

    @staticmethod
    def get_file(path_obj: PurePath) -> Any:
        """Create a filetype specific file object"""
        cls = BaseFile
        for FileClass in cls.__subclasses__():
            try:
                return FileClass(path_obj)
            except FileTypeError:
                continue
        return None

    def create_folders(self) -> None:
        """Create new folders.

        Returns:None

        """
        # [ ] Review add possiblity to create new folders (input arg: new foldername)
        os.makedirs(self.dir, exist_ok=True)

    def exist_path(self) -> bool:
        """Check if the current path exists.

        Returns: Boolean

        """
        return os.path.exists(self.dir)

    def exist_file(self) -> bool:
        """Check if the current file exists.

        Returns: Boolean

        """
        return os.path.isfile(self.fullpath)

    def set_dir(self, subdir: str) -> str:
        """Create the dir path"""
        return os.path.join(self.wkd, subdir)

    def set_fullpath(self) -> None:
        """Create the fullpath to the current file."""
        self.fullpath = os.path.join(self.dir, self.active_filename)

    def get_all_files(self, recursive: bool = False) -> None:
        """Get all files in current folder.

        Returns: List of filenames

        """
        # [ ] REVIEW: @AH show the list of all files with numbers
        # -> user can set a file active in two ways: specifying the name or the number
        if recursive:
            pathfiles = []
            for dirpath, _, fs in os.walk(self.dir, topdown=True):
                for file in fs:
                    pathfiles.append(PurePath(os.path.join(dirpath, file)))
        else:
            pathfiles = [PurePath(entry.path) for entry in os.scandir(self.dir) if entry.is_file()]

        for pf in pathfiles:
            self.files[pf.name] = self.get_file(pf)
        # return [self.get_file(f) for f in files]

    def get_all_subfolders(self) -> list:
        """Get all folder names in current folder"""

        l = []
        startpath = self.dir
        for root, _, files in os.walk(startpath):
            base = root.replacstartpath, "")
            if len(base) > 1:
                if len(files) > 0:
                    l.append((base, files))
        return l

    def contain_files(self) -> bool:
        """Checks if folder contains any file"""
        answer = False
        for _, _, files in os.walk(self.dir):
            if files:
                answer = True
                break

        return answer

    def remove_file(self) -> None:
        """Remove the current file."""
        if not self.active_filename:
            os.remove(self.fullpath)

    def remove_all_files(self) -> None:
        """Remove all files in the active directory"""
        shutil.rmtree(self.dir)
        os.mkdir(self.dir)


if __name__ == "__main__":
    import tempfile

    tmp = tempfile.gettempdir()
    f = FileHandler(filename="test.sh", wkd=tmp, subdir="test")
