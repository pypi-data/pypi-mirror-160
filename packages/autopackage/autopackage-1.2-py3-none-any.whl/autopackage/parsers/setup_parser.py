# encoding:utf-8


import shutil
from enum import Enum

from autopackage.program.statics import Statics


class SetupParser:
    def __init__(self, name, version, author, packages, license, keywords, classifiers, author_email='', description='', long_description='', long_description_content_type='', maintainer='',
                 maintainer_email='', platforms=('any',), url='', download_url='', py_modules=(), zip_safe=False, entry_points=(), install_requires=(), python_requires='', package_data={},
                 data_files=()):
        self.name = name
        self.version = version
        self.author = author
        self.author_email = author_email
        self.maintainer = maintainer
        self.maintainer_email = maintainer_email
        self.license = license
        self.keywords = keywords
        self.classifiers = classifiers
        self.platforms = platforms
        self.description = description
        self.long_description = long_description
        self.long_description_content_type = long_description_content_type
        self.url = url
        self.download_url = download_url
        self.packages = packages
        self.py_modules = py_modules
        self.zip_safe = zip_safe
        self.entry_points = entry_points
        self.install_requires = install_requires
        self.python_requires = python_requires
        self.package_data = package_data
        self.data_files = data_files
        self.top_package = min(self.packages, key=len)
        Statics.PROGRAM_CONFIG = self


class MainModuleLocation(Enum):
    INSIDE = 1
    TOP = 2


def move_main_module(src: MainModuleLocation, dst: MainModuleLocation):
    """
    Moves the main module to the selected location.
    """
    assert src is not dst
    top_path = Statics.SETUP_DIR.joinpath(Statics.MAIN_PATH.name)
    src, dst = (Statics.MAIN_PATH, top_path) if src is MainModuleLocation.INSIDE else (top_path, Statics.MAIN_PATH)
    if src.is_file():
        shutil.move(src, dst)
    else:
        raise FileNotFoundError(f'File {src} not found')
