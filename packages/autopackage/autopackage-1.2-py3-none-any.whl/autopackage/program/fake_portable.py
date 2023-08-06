# encoding:utf-8


import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path
from random import SystemRandom
from tempfile import TemporaryDirectory
from zipfile import ZipFile


def fix_path() -> Path:
    zip_real_path = Path(__file__).resolve().parent
    sys.path[0] = str(zip_real_path)
    return zip_real_path


zip_path = fix_path()
signal.signal(signal.SIGINT, lambda x, y: None)
signal.signal(signal.SIGTERM, lambda x, y: None)


class FakePortable:
    def __init__(self):
        umask = os.umask(0)
        self.__top_package = None
        self.temp_dir: TemporaryDirectory = TemporaryDirectory(suffix='-{0}-{1}'.format(self.top_package, SystemRandom().getrandbits(32)))
        self.temp_dir_path: Path = Path(self.temp_dir.name).resolve()
        self.extract_all()
        os.umask(umask)
        self.run_script()

    @property
    def top_package(self) -> str:
        if self.__top_package is None:
            with ZipFile(zip_path) as myzip:
                files = (file for file in myzip.namelist() if file.count('/'))
                top = min(files, key=len)
                self.__top_package = top.split('/')[0]
        return self.__top_package

    def extract_all(self):
        with ZipFile(zip_path) as myzip:
            myzip.extractall(self.temp_dir_path)
        self.temp_dir_path.joinpath('__main__.py').unlink()
        shutil.move(self.temp_dir_path.joinpath('__main2__.py'), self.temp_dir_path.joinpath('__main__.py'))

    def run_script(self):
        args = sys.argv[1:]
        with self.temp_dir:
            subprocess.run(['python3', str(self.temp_dir_path.joinpath('__main__.py')), *args])
        sys.exit(0)


f = FakePortable()
