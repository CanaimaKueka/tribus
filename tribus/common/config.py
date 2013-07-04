#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append('/media/desarrollo/tribus/')


def readconfig(filename, options=[], conffile=False, strip_comments=True):
    f = open(filename)

    if conffile:
        options = {}
    else:
        options = []

    for line in f:
        line = line.replace('\n', ' ')
        line = line.replace('\t', ' ')
        if '#' in line and strip_comments:
            line, comment = line.split('#', 1)
        if '=' in line and conffile:
            option, value = line.split('=', 1)
            options[option.strip()] = value.strip()
        elif line and not conffile:
            options.append(line.strip())

    f.close()
    return options


def get_classifiers(f):
    return readconfig(f, conffile=False)


def get_repositories(f, l=[]):
    from tribus.common.validators import is_valid_url
    l = []
    for r in readconfig(f, conffile=False):
        if '#egg=' in r and is_valid_url(r):
            l.append(r)
    return l


def get_dependencies(f, l=[]):
    l = []
    for r in readconfig(f, conffile=False, strip_comments=False):
        if '#egg=' in r:
            l.append(r.split('#egg=')[1])
        else:
            l.append(r)
    return l


def get_packages(path, exclude_packages=[], packages=[]):
    from tribus.common.utils import get_split_path, get_path

    if os.path.isfile(get_path([path, '__init__.py'])):
        strippath = get_path([path, '..'])
    else:
        strippath = path
    for dirpath, dirnames, filenames in os.walk(path):
        if '__init__.py' in filenames:
            if dirpath.startswith(strippath):
                dirpath = dirpath[len(strippath):]
            package_name = '.'.join(get_split_path(dirpath))
            packages.append(package_name)
    dummy_list = packages
    for p in dummy_list:
        for e in exclude_packages:
            if p.startswith(e):
                packages.remove(p)
    return packages


def get_package_data(path, exclude_packages=[], exclude_files=[]):
    from tribus.common.utils import get_split_path, get_path

    if os.path.isfile(get_path([path, '__init__.py'])):
        strippath = get_path([path, '..'])
    else:
        strippath = path
    for dirpath, dirnames, filenames in os.walk(path):
        if '__init__.py' in filenames:
            if dirpath.startswith(strippath):
                dirpath = dirpath[len(strippath):]
            package_name = '.'.join(get_split_path(dirpath))
            packages.append(package_name)
    dummy_list = packages
    for p in dummy_list:
        for e in exclude_packages:
            if p.startswith(e):
                packages.remove(p)
    return packages


def get_data_files(path, patterns, d=[], exclude_files=[]):
    """
    Generate a pair of (directory, file-list) for installation.

    'd' -- A directory
    'e' -- A glob pattern
    """
    from tribus.common.utils import find_files, get_path
    d = []
    for l in patterns:
        src, rgx, dest = l.split()
        d.append((dest, find_files(basedir=get_path([path, src]),
                                   pattern=rgx)))
    return d


def get_setup_data(basedir):
    from tribus.common.version import get_version
    from tribus.config.base import NAME, VERSION, URL, AUTHOR, AUTHOR_EMAIL, DESCRIPTION, LICENSE
    from tribus.config.pkg import (classifiers, long_description, install_requires, dependency_links,
                                   exclude_packages, exclude_sources, exclude_patterns,
                                   include_data_patterns)
    return {
        'name': NAME,
        'version': get_version(VERSION),
        'url': URL,
        'author': AUTHOR,
        'author_email': AUTHOR_EMAIL,
        'description': DESCRIPTION,
        'license': LICENSE,
        'packages': get_packages(exclude_packages=exclude_packages, path=basedir),
        # 'package_data': get_package_data(exclude_packages=exclude_packages,
        #                                  exclude_files=exclude_sources+exclude_patterns,
        #                                  path=basedir),
        'data_files': get_data_files(path=basedir, patterns=include_data_patterns,
                                     exclude_files=exclude_sources+exclude_patterns),
        'classifiers': classifiers,
        'long_description': long_description,
        'install_requires': install_requires,
        'dependency_links': dependency_links,
        'zip_safe': False,
    }

if __name__ == '__main__':
    # from tribus.common.utils import find_files, get_path
    from tribus.config.pkg import exclude_sources, exclude_patterns, include_data_patterns
    s = get_data_files(path='/media/desarrollo/tribus/', patterns=include_data_patterns,
                       exclude_files=exclude_sources+exclude_patterns)

    # s = find_files(basedir=get_path(['/media/desarrollo/tribus/', 'tribus/cli']), pattern='*.*')
    print s
