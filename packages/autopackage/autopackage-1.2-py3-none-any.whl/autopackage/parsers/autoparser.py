# encoding:utf-8


import os
import runpy
import sys
from argparse import ArgumentParser, FileType
from pathlib import Path

from autopackage.program.statics import Statics


class AutoParser:
    def __init__(self):
        self.fake_portable = None

        parser = ArgumentParser(description='Easily package your software into a single embedded distributable binary')
        parser.add_argument('-p', '--portable', action='store_true', default=False, help='Define whether the program should be packaged as portable')
        parser.add_argument('-s', '--setup', type=FileType('r'), help='The setup.py file of the project to be packaged', required=True)

        self.args = parser.parse_args()
        self.run()

    def run(self):
        Statics.SETUP_MODULE = Path(self.args.setup.name).resolve()
        Statics.SETUP_DIR = Statics.SETUP_MODULE.parent
        Statics.RELEASES_DIR = Statics.SETUP_DIR.joinpath('releases')
        os.chdir(Statics.SETUP_DIR)  # This is what makes the find_packages() function of the setup.py module work correctly
        runpy.run_path(str(Statics.SETUP_MODULE), run_name=str(Statics.SETUP_MODULE))  # Run setup.py to fill the PROGRAM_CONFIG object
        sys.argv = [str(Statics.SETUP_MODULE), 'bdist_wheel']


def autoparse():
    autoparser = AutoParser()
    Statics.MAIN_PATH = Statics.SETUP_DIR.joinpath(Statics.PROGRAM_CONFIG.top_package).joinpath('__main__.py')
    autoparser.fake_portable = autoparser.args.portable and not Statics.PROGRAM_CONFIG.zip_safe
    return autoparser
