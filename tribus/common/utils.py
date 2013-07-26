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
    return os.path.join(*package.split('.'))


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