# encoding:utf-8


import os
import re
import shutil
import sys
import zipfile

from enum import Enum
from pathlib import Path
from tempfile import mkstemp, NamedTemporaryFile
from typing import Tuple
from zipfile import ZipFile


def is_sudo():
    return os.geteuid() == 0


def remove_portable_metadata(zip_file: Path):
    """
    Removes the dist-info folder from the zip_file to prevent it from being installed
    """
    regexs = (re.compile(r'^(?:.+?)\.dist-info/')), re.compile(r'^EGG-INFO/')
    zin = zipfile.ZipFile(zip_file, 'r')
    with NamedTemporaryFile() as zout:
        zout_path = Path(zout.name).resolve()
    zout = zipfile.ZipFile(zout_path, 'w')
    for item in zin.infolist():
        if re.search(regexs[0], item.filename) is None and re.search(regexs[1], item.filename) is None:
            buffer = zin.read(item.filename)
            zout.writestr(item, buffer)
    zout.close()
    zin.close()
    zip_file.unlink()
    shutil.move(zout_path, zip_file)


class ProgramType(Enum):
    INSTALLED_OR_DEVELOP = 1
    ZIP = 2
    FAKE_PORTABLE = 3


def fix_syspath(main_file_attr: str) -> Tuple[ProgramType, Path]:
    """
    If autopackage is running from a zip file, it adds the full path of the zip file to the sys.path, instead of just a relative path
    If it's running as an installed program or a fake portable program (/temp folder), it adds the full path of the folder containing the __main__.py file to the sys.path
    If it's running from developing code, it adds __main__.py → parent → parent to the sys.path
    :param main_file_attr: The __file__ attribute of the __main__ module
    :return: A 2-tuple containing the ProgramType and the corresponding path described above
    """
    main_path = Path(main_file_attr).resolve()
    dir_candidate = main_path.parent
    zip_file = not main_path.is_file()
    if zip_file:
        if str(dir_candidate) not in sys.path:
            sys.path[0] = str(dir_candidate)
        return ProgramType.ZIP, dir_candidate
    folders = (entry.name for entry in dir_candidate.iterdir() if entry.is_dir())
    top_package = min(folders, key=len)
    regex = re.compile(r'-{0}-\d+?/__main__\.py$'.format(top_package))
    match = re.search(regex, str(main_path))
    if match:
        if str(dir_candidate) not in sys.path:
            sys.path.insert(0, str(dir_candidate))
        return ProgramType.FAKE_PORTABLE, dir_candidate
    root = Path(dir_candidate).resolve().parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return ProgramType.INSTALLED_OR_DEVELOP, root


def extract_single_file(zip_file: Path, inner_file_rel_path: str, dst: Path):
    with ZipFile(zip_file) as myzip:
        with myzip.open(inner_file_rel_path) as myfile, open(dst, 'wb') as destination:
            shutil.copyfileobj(myfile, destination)
