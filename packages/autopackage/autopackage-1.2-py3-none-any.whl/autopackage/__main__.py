#!/usr/bin/env python3
# encoding:utf-8


import glob
import os
import re
import shutil
import sys
from pathlib import Path

from setuptools import setup

# Borrar la siguiente línea
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from autopackage.parsers.autoparser import autoparse
from autopackage.parsers.setup_parser import MainModuleLocation, move_main_module
from autopackage.program.statics import Statics
from autopackage.utils.utils import extract_single_file, remove_portable_metadata

Statics.set_autopackage_dir(__file__)


def main():
    autoparser = autoparse()

    # If the program to be packaged is a fake portable
    if autoparser.fake_portable:
        move_main_module(MainModuleLocation.INSIDE, MainModuleLocation.TOP)
        Statics.PROGRAM_CONFIG.py_modules = ('__main__', '__main2__')
        shutil.move(Statics.SETUP_DIR.joinpath(Statics.MAIN_PATH.name), Statics.SETUP_DIR.joinpath('__main2__.py'))

        # If autopackage is running from a zip file
        if Statics.IS_ZIP:
            extract_single_file(Statics.AUTOPACK_DIR, Statics.FAKE_PORTABLE_MODULE_PATH, Statics.SETUP_DIR.joinpath(Statics.MAIN_PATH.name))

        # Then, it can be running either from a fake portable path or an installed location
        else:
            shutil.copyfile(Statics.AUTOPACK_DIR.joinpath(Statics.FAKE_PORTABLE_MODULE_PATH), Statics.SETUP_DIR.joinpath(Statics.MAIN_PATH.name))

    # If the program to be packaged is portable
    elif autoparser.args.portable:
        move_main_module(MainModuleLocation.INSIDE, MainModuleLocation.TOP)
        Statics.PROGRAM_CONFIG.py_modules = ('__main__',)

    # If it's not portable, then it's installable
    try:
        setup(
            name=Statics.PROGRAM_CONFIG.name,
            version=Statics.PROGRAM_CONFIG.version,
            description=Statics.PROGRAM_CONFIG.description,
            long_description=Statics.PROGRAM_CONFIG.long_description,
            long_description_content_type=Statics.PROGRAM_CONFIG.long_description_content_type,
            author=Statics.PROGRAM_CONFIG.author,
            author_email=Statics.PROGRAM_CONFIG.author_email,
            maintainer=Statics.PROGRAM_CONFIG.maintainer,
            maintainer_email=Statics.PROGRAM_CONFIG.maintainer_email,
            url=Statics.PROGRAM_CONFIG.url,
            download_url=Statics.PROGRAM_CONFIG.download_url,
            license=Statics.PROGRAM_CONFIG.license,
            keywords=Statics.PROGRAM_CONFIG.keywords,
            packages=Statics.PROGRAM_CONFIG.packages,
            py_modules=Statics.PROGRAM_CONFIG.py_modules,
            zip_safe=Statics.PROGRAM_CONFIG.zip_safe,
            classifiers=Statics.PROGRAM_CONFIG.classifiers,
            platforms=Statics.PROGRAM_CONFIG.platforms,
            entry_points=Statics.PROGRAM_CONFIG.entry_points,
            install_requires=Statics.PROGRAM_CONFIG.install_requires,
            python_requires=Statics.PROGRAM_CONFIG.python_requires,
            package_data=Statics.PROGRAM_CONFIG.package_data,
            data_files=Statics.PROGRAM_CONFIG.data_files,
        )

    except SystemExit as sysexit:
        print(sysexit.args[0])

    # We create the releases folder if it doesn't exist and we look for the newly created file
    Statics.RELEASES_DIR.mkdir(parents=True, exist_ok=True)
    created_pkg = glob.iglob(f"{Statics.SETUP_DIR.joinpath('dist')}/*")
    created_pkg = next(created_pkg, None)
    # We make sure the package has been created
    if created_pkg is not None:
        created_pkg = Path(created_pkg).resolve()

        if autoparser.fake_portable:
            Statics.SETUP_DIR.joinpath(Statics.MAIN_PATH.name).unlink()
            shutil.move(Statics.SETUP_DIR.joinpath('__main2__.py'), Statics.SETUP_DIR.joinpath(Statics.MAIN_PATH.name))

        if autoparser.args.portable:
            # We remove the extension and the package metadata
            created_pkg = shutil.move(created_pkg, created_pkg.with_suffix(''))
            remove_portable_metadata(created_pkg)

            # We add the execution header
            print('setting execution permissions to file ' + created_pkg.name)
            os.system(str.format("echo '#!/usr/bin/env python3' | cat - {0} > temp && mv temp {0} ; chmod +x {0}", re.escape(str(created_pkg))))

        # We move the package to the releases folder, overwriting any other file with the same name if necessary
        created_pkg = created_pkg.name
        if Statics.RELEASES_DIR.joinpath(created_pkg).exists():
            Statics.RELEASES_DIR.joinpath(created_pkg).unlink()
        shutil.move(str(Statics.SETUP_DIR.joinpath('dist').joinpath(created_pkg)), str(Statics.RELEASES_DIR))

    # We put the __main__ module back in its package and we remove all the folders created during the packaging process
    if autoparser.args.portable:
        move_main_module(MainModuleLocation.TOP, MainModuleLocation.INSIDE)
    shutil.rmtree(Statics.SETUP_DIR.joinpath('build'), ignore_errors=True)
    shutil.rmtree(Statics.SETUP_DIR.joinpath('dist'), ignore_errors=True)
    egg_info_dir = next(glob.iglob(f'{Statics.SETUP_DIR}/*.egg-info'), None)
    if egg_info_dir is not None:
        shutil.rmtree(egg_info_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
