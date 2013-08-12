#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import inspect
import fnmatch

from tribus.common.logger import get_logger
from tribus.common.utils import (norm_path, find_files, path_to_package, find_dirs,
                                 get_path, list_files, package_to_path, flatten_list,
                                 readconfig)

log = get_logger()

def get_classifiers(filename):
    return readconfig(filename, conffile=False)


def get_dependency_links(filename):
    dependency_links = []
    for line in readconfig(filename, conffile=False):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))
    return dependency_links


def get_requirements(filename, l=[]):
    requirements = []
    for line in readconfig(filename, conffile=False, strip_comments=False):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line).strip())
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line.strip())
    return requirements


def get_packages(path, exclude_packages=[]):
    """
    Returns a list all python packages found within directory 'path', with
    'exclude_packages' packages excluded.

    'where' should be supplied as a "cross-platform" (i.e. URL-style) path; it
    will be converted to the appropriate local path syntax.  'exclude' is a
    sequence of package names to exclude; '*' can be used as a wildcard in the
    names, such that 'foo.*' will exclude all subpackages of 'foo' (but not
    'foo' itself).
    """
    __fname__ = inspect.stack()[0][3]
    packages = []
    path = norm_path(path)
    for init in find_files(path=path, pattern='__init__.py'):
        include = True
        package = path_to_package(os.path.dirname(init).replace(path+os.sep, ''))
        for exclude in exclude_packages+['ez_setup', 'distribute_setup']:
            if fnmatch.fnmatch(package, exclude+'*'):
                include = False
        if include:
            packages.append(package)
            log.debug("[%s.%s] Including package \"%s\" in package list." % (__name__, __fname__, package))
        else:
            log.debug("[%s.%s] Skipping package \"%s\" because of exclude patterns." % (__name__, __fname__, package))
    return filter(None, packages)


def get_package_data(path, packages, data_files, exclude_packages=[], exclude_files=[]):
    """
    For a list of packages, find the package_data

    This function scans the subdirectories of a package and considers all
    non-submodule subdirectories as resources, including them in
    the package_data

    Returns a dictionary suitable for setup(package_data=<result>)
    """
    __fname__ = inspect.stack()[0][3]
    path = norm_path(path)
    package_data = {}
    for package in packages:
        package_data[package] = []
        for f in find_files(path=get_path([path, package_to_path(package)]), pattern='*.*'):
            package_data[package].append(f)
            for e in exclude_packages+['ez_setup', 'distribute_setup']:
                if fnmatch.fnmatch(f, get_path([path, package_to_path(e), '*'])) \
                   and f in package_data[package]:
                    package_data[package].remove(f)
            for x in exclude_files+['*.py']:
                if fnmatch.fnmatch(f, get_path([path, x])) \
                   and f in package_data[package]:
                    package_data[package].remove(f)
        package_data[package] = list(set(package_data[package]) - set(flatten_list(list(zip(*data_files)[1]))))
        for i, j in enumerate(package_data[package]):
            package_data[package][i] = package_data[package][i].replace(path+os.sep+package_to_path(package)+os.sep, '')
    return package_data


def get_data_files(path, patterns, exclude_files=[]):
    """
    Returns a list of pairs (directory, file-list) ready for use
    in setup(data_files=...) (distutils, setuptools, distribute, ...).

    path:
        The path where the files reside. Generally the top level
        directory of the project. Patterns will be expanded in
        this directory.

    patterns:
        This is a list of strings in the form of::
            [
                'relative/path/inside/project *.some.*regex* /dest',
                'another/path/inside/project *.foo.*regex* /dest2',
            ]
        Which means: "Put every file from this folder matching the regex
        inside this other folder".

    exclude_files:
        This is a list of file patterns to exclude from the results.
    """
    __fname__ = inspect.stack()[0][3]
    path = norm_path(path)
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
            d.append((dest+subdir.replace(os.path.join(path, src), ''), f))
            log.debug("[%s.%s] Adding files to install on \"%s\"." % (__name__, __fname__, get_path([dest, subdir])))
    return d


def get_setup_data(basedir):
    from tribus.config.base import NAME, VERSION, URL, AUTHOR, AUTHOR_EMAIL, DESCRIPTION, LICENSE, DOCDIR
    from tribus.config.pkg import (classifiers, long_description, install_requires, dependency_links,
                                   exclude_packages, platforms, keywords)
    from tribus.common.version import get_version
    from tribus.common.setup.build import build_man, build_img, build_sphinx, compile_catalog, build
    from tribus.common.setup.clean import clean_mo, clean_sphinx, clean_man, clean_img, clean_dist, clean
    from tribus.common.setup.install import install_data, build_py
    from tribus.common.setup.maint import extract_messages, init_catalog, update_catalog

    packages = get_packages(path=basedir, exclude_packages=exclude_packages)

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
        'packages': packages,
        'data_files': [('', [])],               # data_files is empty because it is filled during execution of install_data
        'package_data': {'': []},               # package_data is empty because it is filled during execution of build_py
        'install_requires': install_requires,
        'dependency_links': dependency_links,
        'zip_safe': False,
        'cmdclass': {
            'clean': clean,
            'clean_dist': clean_dist,
            'clean_img': clean_img,
            'clean_mo': clean_mo,
            'clean_man': clean_man,
            'clean_sphinx': clean_sphinx,
            'build': build,
            'build_img': build_img,
            'build_man': build_man,
            'build_py': build_py,
            'build_sphinx': build_sphinx,
            'compile_catalog': compile_catalog,
            'init_catalog': init_catalog,
            'update_catalog': update_catalog,
            'extract_messages': extract_messages,
            'install_data': install_data,
        },
        'message_extractors': {
            'tribus': [
                ('**.html', 'tribus.common.setup.message_extractors:django', ''),
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
                'domain': ('setup.py', 'tribus'),
                'input_file': ('setup.py', 'tribus/i18n/pot/tribus.pot'),
                'output_dir': ('setup.py', 'tribus/i18n'),
            },
            'compile_catalog': {
                'domain': ('setup.py', 'tribus'),
                'directory': ('setup.py', 'tribus/i18n'),
                'use_fuzzy': ('setup.py', True),
            },
            'init_catalog': {
                'domain': ('setup.py', 'tribus'),
                'input_file': ('setup.py', 'tribus/i18n/pot/tribus.pot'),
                'output_dir': ('setup.py', 'tribus/i18n'),
            },
            'extract_messages': {
                # 'add_comments': ('setup.py', 'TRANSLATOR:'),
                'copyright_holder': ('setup.py', 'Desarrolladores de Tribus'),
                'msgid_bugs_address': ('setup.py', 'desarrolladores@canaima.softwarelibre.gob.ve'),
                'output_file': ('setup.py', 'tribus/i18n/pot/tribus.pot'),
                # 'keywords': ('setup.py', '_'),
                'charset': ('setup.py', 'utf-8'),
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