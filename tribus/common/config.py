#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ConfigParser

sys.path.append('/media/desarrollo/tribus/')


def readconfig(filename, options=[], conffile=False):
    f = open(filename)

    if conffile:
        options = {}
    else:
        options = []

    optionchar = '='
    commentchar = '#'

    for line in f:
        line = line.strip('\n')
        if commentchar in line:
            line, comment = line.split(commentchar, 1)
        if optionchar in line and conffile:
            option, value = line.split(optionchar, 1)
            options[option.strip()] = value.strip()
        elif optionchar not in line and conffile:
            options['orphaned'].append(line.strip())
        else:
            options.append(line.strip())

    f.close()
    return options


def ConfigMapper(confdir):
    from tribus.common.utils import get_listdir_fullpath

    dictionary = {}
    config = ConfigParser.ConfigParser()
    conffiles = get_listdir_fullpath(confdir)
    configuration = config.read(conffiles)
    sections = config.sections()
    for section in sections:
        options = config.options(section)
        for option in options:
            try:
                giveme = config.get(section, option)
                if section == 'array':
                    process = giveme[1:-1].split(',')
                elif section == 'boolean':
                    process = giveme
                elif section == 'integer':
                    process = int(giveme)
                else:
                    process = '"'+giveme+'"'
                dictionary[option] = process
            except:
                dictionary[option] = None
    return dictionary


def get_classifiers(f):
    from tribus.common.utils import get_file_on_list
    return get_file_on_list(f)


def get_repositories(f, l=[]):
    from tribus.common.validators import is_valid_url
    l = []
    for r in open(f):
        if '#egg=' in r and is_valid_url(r):
            l.append(r)
    return l


def get_dependencies(f, l=[]):
    l = []
    for r in open(f):
        if '#egg=' in r:
            l.append(r.split('#egg=')[1])
        else:
            l.append(r)
    return l


def get_packages(path, exclude_packages=[], packages=[]):
    from tribus.common.utils import get_split_path, get_path

    if os.path.isfile(get_path([path, '__init__.py'])):
        strippath = get_path([path, '..'])
        print strippath
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
    return []
    # from tribus.common.utils import get_split_path

    # for dirpath, dirnames, filenames in os.walk(path):
    #     parts = get_split_path(dirpath)
    #     package_name = '.'.join(parts)
    #     if '__init__.py' in filenames:
    #         packages.append(package_name)
    #     elif filenames:
    #         relative_path = []
    #         while '.'.join(parts) not in packages:
    #             relative_path.append(parts.pop())
    #         relative_path.reverse()
    #         path = os.path.join(*relative_path)
    #         package_files = package_data.setdefault('.'.join(parts), [])
    #         package_files.extend([os.path.join(path, f) for f in filenames])
    # return package_files, package_data, packages


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
        d.append([dest, find_files(basedir=get_path([path, src]),
                                   pattern=rgx)])
    return d


def get_setup_data(basedir):
    from tribus.common.version import get_version
    from tribus.config.base import NAME, VERSION, URL, AUTHOR, AUTHOR_EMAIL, DESCRIPTION, LICENSE
    from tribus.config.pkg import (classifiers, long_description, requires, dependency_links,
                                   exclude_packages, exclude_sources, exclude_patterns,
                                   include_data_patterns)
    print requires
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
        'requires': requires,
        'dependency_links': dependency_links,
        'zip_safe': False,
    }

if __name__ == '__main__':
    s = get_setup_data('/media/desarrollo/tribus/')
    print s
