# encoding:utf-8


from pathlib import Path

from autopackage.utils.utils import fix_syspath, ProgramType


class Statics:
    AUTOPACK_DIR: Path = None  # The absolute path to the running zip file, the fake portable running folder or the installed folder. Never ends with '/' .
    IS_FAKE_PORTABLE = None  # autopackage is running as a fake portable (temp folder)
    IS_ZIP: bool = not Path(__file__).resolve().is_file()  # autopackage is running from a zip file
    FAKE_PORTABLE_MODULE_PATH = 'autopackage/program/fake_portable.py'
    SETUP_MODULE: Path = None
    SETUP_DIR: Path = None
    MAIN_PATH: Path = None
    PROGRAM_CONFIG = None
    RELEASES_DIR: Path = None

    @classmethod
    def set_autopackage_dir(cls, main_file_attr):
        programtype, path = fix_syspath(main_file_attr)
        cls.AUTOPACK_DIR = path
        cls.IS_FAKE_PORTABLE = programtype is ProgramType.FAKE_PORTABLE
