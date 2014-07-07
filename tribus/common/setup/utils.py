#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

tribus.common.setup.utils
=========================

This module contains common functions to process the information needed
by Setuptools/Distutils setup script.

"""

import os
import re
import fnmatch

from tribus.common.logger import get_logger
from tribus.common.utils import (
    find_files, path_to_package, find_dirs,
    get_path, list_files, package_to_path, flatten_list,
    readconfig)

log = get_logger()


def get_classifiers(filename=None):
    """

    Reads python classifiers from a file.

    :param filename: a filename containing python classifiers
                     (one classifier per line).
    :return: a list with each classifier.
    :rtype: ``list``

    .. versionadded:: 0.1

    """

    assert filename
    return readconfig(filename, conffile=False)


# TODO: Inspired from:
#
def get_dependency_links(filename=None):
    """

    Procesess dependency links from a requirements file
    or a simple pip dependency file.

    :param filename: a filename containing python packages
                     in a format expected by pip (one per line).
    :return: a list of dependency links.
    :rtype: ``list``

    .. versionadded:: 0.1

    """
    assert filename is not None
    dependency_links = []
    for line in readconfig(filename, conffile=False):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))
    return dependency_links


# TODO: Inspired from:
#
def get_requirements(filename=None):
    """
    Procesess dependencies from a requirements file
    or a simple pip dependency file.

    :param filename: a filename containing python packages
                     in a format expected by pip (one per line).
    :return: a list of dependencies (python packages).
    :rtype: ``list``

    .. versionadded:: 0.1
    """
    assert filename is not None
    requirements = []
    for line in readconfig(filename, conffile=False, strip_comments=False):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(
                re.sub(
                    r'\s*-e\s+.*#egg=(.*)$',
                    r'\1',
                    line).strip(
                    ))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line.strip())
    return requirements


def get_packages(path=None, exclude_packages=[]):
    """
    Returns a list of all python packages found within directory ``path``, with
    ``exclude_packages`` packages excluded.

    :param path: the path where the packages will be searched. It should
                 be supplied as a "cross-platform" (i.e. URL-style) path; it
                 will be converted to the appropriate local path syntax.
    :param exclude_packages: is a sequence of package names to exclude;
                             ``*`` can be used as a wildcard in the names,
                             such that ``foo.*`` will exclude all subpackages
                             of ``foo`` (but not ``foo`` itself).
    :return: a list of packages.
    :rtype: ``list``

    .. versionadded:: 0.1
    """
    assert path
    assert exclude_packages
    assert type(path) == str
    assert type(exclude_packages) == list
    pkgs = []
    path = os.path.normpath(path)
    for init in find_files(path=path, pattern='__init__.py'):
        include = True
        pkg = path_to_package(os.path.dirname(init).replace(path + os.sep, ''))
        for exclude in exclude_packages:
            if fnmatch.fnmatch(pkg, exclude + '*'):
                include = False
        if include:
            pkgs.append(pkg)
    return filter(None, pkgs)


def get_package_data(path=None, packages=None, data_files=None,
                     exclude_packages=None, exclude_files=None):
    """
    For a list of packages, find the package_data

    This function scans the subdirectories of a package and considers all
    non-submodule subdirectories as resources, including them in
    the package_data

    Returns a dictionary suitable for setup(package_data=<result>)
    """
    assert path is not None
    assert packages is not None
    assert data_files is not None
    path = os.path.normpath(path)
    package_data = {}
    for package in packages:
        package_data[package] = []
        for f in find_files(path=get_path([path, package_to_path(package)]), pattern='*.*'):
            package_data[package].append(f)
            for e in exclude_packages + ['ez_setup', 'distribute_setup']:
                if fnmatch.fnmatch(f, get_path([path, package_to_path(e), '*'])) \
                   and f in package_data[package]:
                    package_data[package].remove(f)
            for x in exclude_files + ['*.py']:
                if fnmatch.fnmatch(f, get_path([path, x])) \
                   and f in package_data[package]:
                    package_data[package].remove(f)
        package_data[package] = list(
            set(package_data[package]) - set(flatten_list(list(zip(*data_files)[1]))))
        for i, j in enumerate(package_data[package]):
            package_data[package][i] = package_data[package][i].replace(path + os.sep + package_to_path(package) + os.sep, '')
    return package_data


def get_data_files(path=None, patterns=None, exclude_files=None):
    """

    Procesess a list of patterns to get a list of files that should be put in
    a directory. This function helps the Tribus Maintainer to define a list of
    files to be installed in a certain system directory.

    For example, generated documentation (everything under
    ``tribus/data/docs/html`` after executing ``make build_sphinx``) should be
    put in ``/usr/share/doc/tribus/``. The maintainer should add a pattern like
    the following so that everything from ``tribus/data/docs/html`` gets copied
    to ``/usr/share/doc/tribus/`` when the package is installed
    (``python setup.py install``) or a binary distribution is created
    (``python setup.py bdist``).

    :param path: the path where the files reside. Generally the top level
                 directory of the project. Patterns will be expanded in
                 this directory.
    :param patterns: this is a list of strings in the form of::

                         ['relative/path/inside/project *.some.*regex* /dest',
                          'another/path/inside/project *.foo.*regex* /dest2',
                          'path/ *.* dest/']

                     which means, *Put every file from this folder matching the
                     regex inside this other folder*.

    :param exclude_files: this is a list of file patterns to exclude from the
                          results.
    :return: a list of pairs ``('directory', [file-list])`` ready for use
             in ``setup(data_files=...)`` from Setuptools/Distutils.
    :rtype: ``list``

    .. versionadded:: 0.1

    """
    assert path is not None
    assert patterns is not None
    path = os.path.normpath(path)
    d = []
    for l in patterns:
        src, rgx, dest = l.split()
        for subdir in find_dirs(path=get_path([path, src])):
            f = []
            for files in list_files(path=subdir):
                f.append(files)
                for exclude in exclude_files:
                    if fnmatch.fnmatch(files, exclude) and files in f:
                        f.remove(files)
            d.append((dest + subdir.replace(os.path.join(path, src), ''), f))
    return d


def get_setup_data(basedir):
    """
    Prepares a dictionary of values to configure python Distutils.

    :param basedir: the path where the files reside. Generally the top level
                    directory of the project.
    :return: a dic
    :rtype: ``dictionary``

    .. versionadded:: 0.1
    """
    from tribus.config.base import (NAME, VERSION, URL, AUTHOR, AUTHOR_EMAIL,
                                    DESCRIPTION, LICENSE, DOCDIR)
    from tribus.config.pkg import (classifiers, long_description,
                                   install_requires, dependency_links,
                                   exclude_packages, platforms, keywords)
    from tribus.common.version import get_version
    from tribus.common.setup.build import (build_man, build_css, build_js,
                                           build_sphinx, compile_catalog,
                                           build)
    from tribus.common.setup.clean import (clean_mo, clean_sphinx, clean_js,
                                           clean_css, clean_man, clean_img,
                                           clean_dist, clean_pyc, clean)
    from tribus.common.setup.install import install_data, build_py
    from tribus.common.setup.maint import (extract_messages, init_catalog,
                                           update_catalog)
    from tribus.common.setup.report import report_setup_data

    return {
        'name': NAME,
        'version': get_version(VERSION),
        'url': URL,
        'author': AUTHOR,
        'author_email': AUTHOR_EMAIL,
        'description': DESCRIPTION,
        'long_description': long_description,
        'license': LICENSE,
        'classifiers': classifiers,
        'keywords': keywords,
        'platforms': platforms,
        'packages': get_packages(path=basedir,
                                 exclude_packages=exclude_packages),
        'data_files': [('', [])],
        'package_data': {'': []},
        'install_requires': install_requires,
        'dependency_links': dependency_links,
        'test_suite': 'tribus.common.testsuite.runtests',
        'zip_safe': False,
        'cmdclass': {
            'clean': clean,
            'clean_dist': clean_dist,
            'clean_img': clean_img,
            'clean_js': clean_js,
            'clean_css': clean_css,
            'clean_mo': clean_mo,
            'clean_man': clean_man,
            'clean_sphinx': clean_sphinx,
            'clean_pyc': clean_pyc,
            'build': build,
            'build_js': build_js,
            'build_css': build_css,
            'build_man': build_man,
            'build_py': build_py,
            'build_sphinx': build_sphinx,
            'compile_catalog': compile_catalog,
            'init_catalog': init_catalog,
            'update_catalog': update_catalog,
            'extract_messages': extract_messages,
            'install_data': install_data,
            'report_setup_data': report_setup_data,
        },
        'message_extractors': {
            'tribus': [
                ('**.html',
                 'tribus.common.setup.message_extractors:django', ''),
                ('**.py', 'python', ''),
            ],
        },
        'command_options': {
            'egg_info': {
                'tag_build': ('setup.py', ''),
                'tag_svn_revision': ('setup.py', False),
            },
            'install': {
                'prefix': ('setup.py', '/usr'),
                'exec_prefix': ('setup.py', '/usr'),
                'install_layout': ('setup.py', 'deb'),
            },
            'update_catalog': {
                'domain': ('setup.py', 'django'),
                'input_file': ('setup.py', 'tribus/data/i18n/pot/django.pot'),
                'output_dir': ('setup.py', 'tribus/data/i18n'),
                'ignore_obsolete': ('setup.py', True),
                'previous': ('setup.py', False),
            },
            'compile_catalog': {
                'domain': ('setup.py', 'django'),
                'directory': ('setup.py', 'tribus/data/i18n'),
                'use_fuzzy': ('setup.py', True),
            },
            'init_catalog': {
                'domain': ('setup.py', 'django'),
                'input_file': ('setup.py', 'tribus/data/i18n/pot/django.pot'),
                'output_dir': ('setup.py', 'tribus/data/i18n'),
            },
            'extract_messages': {
                'copyright_holder': ('setup.py', 'Desarrolladores de Tribus'),
                'msgid_bugs_address':
                ('setup.py',
                    'desarrolladores@canaima.softwarelibre.gob.ve'),
                'output_file': ('setup.py', 'tribus/data/i18n/pot/django.pot'),
                'charset': ('setup.py', 'utf-8'),
                'sort_by_file': ('setup.py', True),
                'no_wrap': ('setup.py', True),
            },
            'build_sphinx': {
                'source_dir': ('setup.py', get_path([DOCDIR, 'rst'])),
                'build_dir': ('setup.py', DOCDIR),
                'fresh_env': ('setup.py', True),
                'all_files': ('setup.py', True),
            },
        },
        'entry_points': {
            'console_scripts': [
                'tbs = tribus.main:main',
            ]
        },
    }
