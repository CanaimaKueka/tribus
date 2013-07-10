#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fnmatch
import inspect
import re

from tribus.common.logger import get_logger

log = get_logger()


def flatten_list(l, limit=1000, counter=0):
    for i in xrange(len(l)):
        if (isinstance(l[i], (list, tuple)) and counter < limit):
            for a in l.pop(i):
                l.insert(i, a)
                i += 1
            counter += 1
            return flatten_list(l, limit, counter)
    return l


def cat_file(filename):
    return open(filename).read()


def norm_path(path):
    if path.endswith(os.sep):
        return os.path.split(path)[0]
    else:
        return path


def get_path(path=[]):
    path[0] = os.path.realpath(os.path.abspath(path[0]))
    return os.path.normpath(os.path.join(*path))


def package_to_path(package):
    """
    Convert a package (as found by setuptools.find_packages)
    e.g. "foo.bar" to usable path
    e.g. "foo/bar"

    No idea if this works on windows
    """
    return get_path(package.split('.'))


def path_to_package(path):
    path = norm_path(path)
    return path.replace(os.sep, '.')


def list_files(path):
    '''
    Returns a list of all files and folders in a directory
    (non-recursive)
    '''
    path = norm_path(path)
    return [get_path([path, f]) for f in os.listdir(path) if os.path.isfile(get_path([path, f]))]


def find_files(path, pattern):
    '''
    Locate all files matching supplied filename pattern in and below
    supplied root directory.
    '''
    d = []
    path = norm_path(path)
    for directory, subdirs, files in os.walk(path):
        for filename in fnmatch.filter(files, pattern):
            d.append(get_path([directory, filename]))
    return d


def list_dirs(path):
    """
    Get the subdirectories within a package
    This will include resources (non-submodules) and submodules
    """
    path = norm_path(path)
    try:
        subdirectories = ['']+os.walk(path).next()[1]
    except StopIteration:
        subdirectories = []
    return subdirectories


def find_dirs(path):
    """
    Get the subdirectories within a package
    This will include resources (non-submodules) and submodules
    """
    path = norm_path(path)
    try:
        subdirectories = [d[0] for d in os.walk(path) if os.path.isdir(d[0])]
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


def get_classifiers(filename):
    return readconfig(filename, conffile=False)


def get_dependency_links(filename):
    from tribus.common.validators import is_valid_url
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
            package_data[package][i] = package_data[package][i].replace(path+os.sep, '')
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
    from babel.messages import frontend as babel
    from tribus.common.version import get_version
    from tribus.common.build import build_html, build_man, build_img, build
    from tribus.common.clean import clean_mo, clean_html, clean_man, clean_img, clean
    from tribus.common.install import install_data
    from tribus.config.base import NAME, VERSION, URL, AUTHOR, AUTHOR_EMAIL, DESCRIPTION, LICENSE
    from tribus.config.pkg import (classifiers, long_description, install_requires, dependency_links,
                                   exclude_packages, exclude_sources, exclude_patterns,
                                   include_data_patterns, platforms, keywords)
    __fname__ = inspect.stack()[0][3]
    packages = get_packages(path=basedir, exclude_packages=exclude_packages)
    data_files = get_data_files(path=basedir, patterns=include_data_patterns,
                                exclude_files=exclude_sources+exclude_patterns)
    package_data = get_package_data(path=basedir, packages=packages, data_files=data_files,
                                    exclude_files=exclude_sources+exclude_patterns,
                                    exclude_packages=exclude_packages)
    log.debug("[%s.%s] All setup data processed and ready to use." % (__name__, __fname__))
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
        'cmdclass': {
            'clean': clean,
            'clean_img': clean_img,
            'clean_mo': clean_mo,
            'clean_man': clean_man,
            'clean_html': clean_html,
            'build': build,
            'build_img': build_img,
            'build_mo': babel.compile_catalog,
            'build_man': build_man,
            'build_html': build_html,
            'install_data': install_data,
            'create_pot': babel.extract_messages,
            'create_po': babel.init_catalog,
            'update_po': babel.update_catalog
        },
    }
