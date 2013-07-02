#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append('/media/desarrollo/tribus/')


def readconfig(filename, optionchar='=', commentchar='#', options=[], conffile=False):
    f = open(filename)

    if conffile:
        options = {}

    for line in f:
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


def get_classifiers(f):
    from tribus.common.utils import get_file_on_list
    return get_file_on_list(f)


def get_repositories(f, l=[]):
    for r in open(f):
        if '#egg=' in r:
            from django.core.validators import URLValidator

            try:
                URLValidator(r)
            except:
                r = ''

            l.append(r)
    return l


def get_dependencies(f, l=[]):
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


# def get_packages_data(path, packages=[], package_data={}):
#     from tribus.common.utils import get_split_path

#     for dirpath, dirnames, filenames in os.walk(path):
#         parts = get_split_path(dirpath)
#         package_name = '.'.join(parts)
#         if '__init__.py' in filenames:
#             packages.append(package_name)
#         elif filenames:
#             relative_path = []
#             while '.'.join(parts) not in packages:
#                 relative_path.append(parts.pop())
#             relative_path.reverse()
#             path = os.path.join(*relative_path)
#             package_files = package_data.setdefault('.'.join(parts), [])
#             package_files.extend([os.path.join(path, f) for f in filenames])
#     return package_files, package_data, packages


def get_data_files(path, f, d=[]):
    """
    Generate a pair of (directory, file-list) for installation.

    'd' -- A directory
    'e' -- A glob pattern
    """
    from tribus.common.utils import find_files, get_path

    for l in readconfig(filename=f, conffile=False):
        src, rgx, dest = l.split()
        d.append([dest, find_files(basedir=get_path([path, src]),
                                   pattern=rgx)])
    return d


def get_setup_data(basedir):
    from tribus.common.utils import get_path, cat_file

    pkgdir = get_path([basedir, 'tribus', 'data', 'pkg'])

    f_readme = get_path([pkgdir, 'README'])
    f_classifiers = get_path([pkgdir, 'python-classifiers.list'])
    f_dependencies = get_path([pkgdir, 'python-dependencies.list'])
    f_exclude_packages = get_path([pkgdir, 'exclude-packages.list'])
    f_exclude_sources = get_path([pkgdir, 'exclude-sources.list'])
    f_exclude_patterns = get_path([pkgdir, 'exclude-patterns.list'])
    f_data_files = get_path([pkgdir, 'data-files.list'])

    exclude_sources = readconfig(filename=f_exclude_sources, conffile=False)
    exclude_packages = readconfig(filename=f_exclude_packages, conffile=False)
    exclude_patterns = readconfig(filename=f_exclude_patterns, conffile=False)

    return dict(
        {
            'packages': get_packages(exclude_packages=exclude_packages, path=basedir),
            # 'packages_data': get_packages_data(exclude_packages=exclude_packages,
            #                                    exclude_files=exclude_sources+exclude_patterns,
            #                                    path=basedir),
            'classifiers': get_classifiers(f=f_classifiers),
            'long_description': cat_file(f=f_readme),
            'data_files': get_data_files(path=basedir, f=f_data_files,
                                         exclude_files=exclude_sources+exclude_patterns),
            'install_requires': get_dependencies(f=f_dependencies),
            'dependency_links': get_repositories(f=f_dependencies),
        },
        **readconfig(filename=get_path([basedir, 'tribus', 'data', 'pkg', 'METADATA']),
                     conffile=True)
    )

if __name__ == '__main__':
    p = get_data_files('/media/desarrollo/tribus/', '/media/desarrollo/tribus/tribus/data/pkg/data-files.list')
    print p
