#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
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

'''

tribus.common.utils
===================

This module contains common and low level functions to all modules in Tribus.

'''

import os
import fnmatch
import hashlib
import urllib
from gettext import gettext as _

from tribus.common.logger import get_logger

log = get_logger()


def flatten_list(l=[], limit=1000, counter=0):
    '''

    Converts a nested list into one combined list.

    :param l: a list object with (optionally) nested list.
    :param limit: the maximum amount of nested lists (recursive).
    :param counter:

    .. versionadded:: 0.1

    '''
    assert l is not None
    assert limit > 0
    assert counter >= 0

    for i in xrange(len(l)):
        if (isinstance(l[i], (list, tuple)) and counter < limit):
            for a in l.pop(i):
                l.insert(i, a)
                i += 1
            counter += 1
            return flatten_list(l, limit, counter)

    log.debug(_('I have flattened a list with %s elements.' % counter))

    return l


def cat_file(filename=None):
    '''

    Outputs the contents of a file.

    :param filename: the file to read from.
    :return: the contents of a file.
    :rtype: a string.

    .. versionadded:: 0.1

    >>> f = open('/tmp/test_cat_file', 'w')
    >>> f.write('This is a test case to see if the contents of a file are outputted the way it\\n should.')
    >>> f.close()
    >>> cat_file('/tmp/test_cat_file')
    'This is a test case to see if the contents of a file are outputted the way it\\n should.'

    '''
    assert filename is not None
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
        subdirectories = [''] + os.walk(path).next()[1]
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

# Taken from
# http://www.joelverhagen.com/blog/2011/02/md5-hash-of-file-in-python/


def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def scan_repository(repo_root):
    '''
    Este metodo lee el archivo distributions ubicado en la raiz de un
    repositorio y genera un diccionario con las distribuciones y
    componentes presentes en dicho repositorio.
    '''

    dist_releases = {}
    dists = urllib.urlopen(os.path.join(repo_root, "distributions"))
    linea = dists.readline().strip("\n")

    while linea:
        l = linea.split(" ")
        dist_releases[l[0]] = l[1]
        linea = dists.readline().strip("\n")

    return dist_releases


def filename_generator(file_parts, new_m_time):
    filename = os.path.basename(file_parts[0])
    url = os.path.dirname(file_parts[0])
    ext = file_parts[1]
    m = hashlib.md5()
    m.update(filename)
    return '{0}/{1}.{2}{3}'.format(url, m.hexdigest(), new_m_time, ext)


def delete_dir(dirname):
    if os.path.isdir(dirname):
        print "Deleting %s" % dirname
        for root, dirs, files in os.walk(dirname, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(dirname)
