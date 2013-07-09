#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fnmatch
import glob
import sys
import inspect

sys.path.append(os.getcwd())

from tribus.common.logger import get_logger

log = get_logger()


# def get_listdir_fullpath(d):
#     '''
#     Returns a list of all files and folders in a directory
#     (non-recursive)
#     '''
#     return [os.path.join(d, f) for f in os.listdir(d)]


def cat_file(f):
    return open(f).read()


def get_path(p=[]):
    p[0] = os.path.realpath(os.path.abspath(p[0]))
    return os.path.normpath(os.path.join(*p))


def package_to_path(package):
    """
    Convert a package (as found by setuptools.find_packages)
    e.g. "foo.bar" to usable path
    e.g. "foo/bar"

    No idea if this works on windows
    """
    return get_path(package.split('.'))


def list_files(d):
    '''
    Returns a list of all files and folders in a directory
    (non-recursive)
    '''
    return [get_path([d, f]) for f in os.listdir(d) if os.path.isfile(get_path([d, f]))]


def find_files(basedir, pattern):
    '''
    Locate all files matching supplied filename pattern in and below
    supplied root directory.
    '''
    d = []
    for path, dirs, files in os.walk(basedir):
        for filename in fnmatch.filter(files, pattern):
            d.append(get_path([path, filename]))
    return d


def find_subdirectories(path):
    """
    Get the subdirectories within a package
    This will include resources (non-submodules) and submodules
    """
    try:
        subdirectories = ['']+os.walk(path).next()[1]
    except StopIteration:
        subdirectories = []
    return subdirectories


# def get_split_path(path, result=None):
#     """
#     Split a pathname into components (the opposite of os.path.join)
#     in a platform-neutral way.
#     """
#     if result is None:
#         result = []
#     head, tail = os.path.split(path)
#     if head == '':
#         return [tail] + result
#     if head == path:
#         return result
#     return get_split_path(head, [tail] + result)


# def get_files_from_pattern(path, pattern):
#     """
#     Generate a pair of (directory, file-list) for installation.

#     'd' -- A directory
#     'e' -- A glob pattern
#     """
#     return [f for f in glob.glob('%s/%s' % (path, pattern)) if os.path.isfile(f)]


# def findall(dir=os.curdir):
#     """
#     Find all files under 'dir' and return the list of full filenames
#     (relative to 'dir').
#     """
#     all_files = []
#     for base, dirs, files in os.walk(dir):
#         if base == os.curdir or base.startswith(os.curdir+os.sep):
#             base = base[2:]
#         if base:
#             files = [os.path.join(base, f) for f in files]
#         all_files.extend(filter(os.path.isfile, files))
#     return all_files


# def subdir_findall(dir, subdir):
#     """
#     Find all files in a subdirectory and return paths relative to dir

#     This is similar to (and uses) setuptools.findall
#     However, the paths returned are in the form needed for package_data
#     """
#     strip_n = len(dir.split('/'))
#     path = '/'.join((dir, subdir))
#     return ['/'.join(s.split('/')[strip_n:]) for s in findall(path)]


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
# def parse_dependency_links(file_name):
#     """
#     from:
#         http://cburgmer.posterous.com/pip-requirementstxt-and-setuppy
#     """
#     dependency_links = []
#     with open(file_name) as f:
#         for line in f:
#             if re.match(r'\s*-[ef]\s+', line):
#                 dependency_links.append(re.sub(r'\s*-[ef]\s+',
#                                                '', line))
#     return dependency_links


def get_dependencies(f, l=[]):
    l = []
    for r in readconfig(f, conffile=False, strip_comments=False):
        if '#egg=' in r:
            l.append(r.split('#egg=')[1])
        else:
            l.append(r)
    return l
# def parse_requirements(file_name):
#     """
#     from:
#         http://cburgmer.posterous.com/pip-requirementstxt-and-setuppy
#     """
#     requirements = []
#     with open(file_name, 'r') as f:
#         for line in f:
#             if re.match(r'(\s*#)|(\s*$)', line):
#                 continue
#             if re.match(r'\s*-e\s+', line):
#                 requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$',
#                                            r'\1', line).strip())
#             elif re.match(r'\s*-f\s+', line):
#                 pass
#             else:
#                 requirements.append(line.strip())
#     return requirements


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
    include = True

    for init in find_files(basedir=path, pattern='__init__.py'):
        package = os.path.dirname(init).replace(path, '').replace(os.sep, '.')
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
    package_data = {}
    for package in packages:
        package_data[package] = []
        for subdir in find_subdirectories(package_to_path(package)):
            if not get_path([package_to_path(package), subdir]).replace(os.sep, '.') in packages:
                package_data[package] += find_files(basedir=get_path([path, package_to_path(package), subdir]),
                                                    pattern='*.*')
    for files in data_files:
        for f in files[1]:
            exclude_files.append(f)

    for p in exclude_packages:
        exclude_files.append(get_path([path, package_to_path(p), '*']))

    for e in exclude_files:
        for k, v in package_data.iteritems():
            for i in v:
                if i in package_data[k] and fnmatch.fnmatch(i, e):
                    package_data[k].remove(i)

    for k, v in package_data.iteritems():
        l = []
        for i in v:
            l.append(i.replace(path, ''))
        package_data[k] = l

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
    d = []
    for l in patterns:
        src, rgx, dest = l.split()
        for subdir in find_subdirectories(path=get_path([path, src])):
            f = []
            for files in list_files(d=get_path([path, src, subdir])):
                f.append(files)
                for exclude in exclude_files:
                    if fnmatch.fnmatch(files, exclude) and files in f:
                        f.remove(files)
            if f:
                d.append((get_path([dest, subdir]), f))
                log.debug("[%s.%s] Adding files to install on \"%s\"." % (__name__, __fname__, get_path([dest, subdir])))
    return d


def get_setup_data(basedir):
    from tribus.common.version import get_version
    from tribus.config.base import NAME, VERSION, URL, AUTHOR, AUTHOR_EMAIL, DESCRIPTION, LICENSE
    from tribus.config.pkg import (classifiers, long_description, install_requires, dependency_links,
                                   exclude_packages, exclude_sources, exclude_patterns,
                                   include_data_patterns, platforms, keywords)

    packages = get_packages(path=basedir, exclude_packages=exclude_packages)
    data_files = get_data_files(path=basedir, patterns=include_data_patterns,
                                exclude_files=exclude_sources+exclude_patterns)
    package_data = get_package_data(path=basedir, packages=packages, data_files=data_files,
                                    exclude_files=exclude_sources+exclude_patterns,
                                    exclude_packages=exclude_packages)
    return {
        'name': NAME,
        'version': get_version(VERSION),
        'url': URL,
        'author': AUTHOR,
        'author_email': AUTHOR_EMAIL,
        'description': DESCRIPTION,
        'license': LICENSE,
        'keywords': keywords,
        'platforms': platforms,
        'packages': packages,
        'data_files': data_files,
        'package_data': package_data,
        'classifiers': classifiers,
        'long_description': long_description,
        'install_requires': install_requires,
        'dependency_links': dependency_links,
        'zip_safe': False,
    }

if __name__ == '__main__':
    from tribus.config.pkg import (classifiers, long_description, install_requires, dependency_links,
                               exclude_packages, exclude_sources, exclude_patterns,
                               include_data_patterns)
    print dependency_links
    packages = get_packages(path='/home/huntingbears/desarrollo/tribus/', exclude_packages=exclude_packages)
    data_files = get_data_files(path='/home/huntingbears/desarrollo/tribus/', patterns=include_data_patterns, exclude_files=exclude_sources+exclude_patterns)
    s = get_package_data(path='/home/huntingbears/desarrollo/tribus/', packages=packages, data_files=data_files, exclude_packages=exclude_packages, exclude_files=exclude_sources+exclude_patterns)
#     d = subdir_findall(dir='/home/huntingbears/desarrollo/tribus/', subdir='tribus')
#     print p
#     print d
#     print s
    # print find_subdirectories(path='/home/huntingbears/desarrollo/tribus/')
    import pprint
    pprint.pprint(s)
