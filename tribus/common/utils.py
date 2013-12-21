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

# TODO: Reference author from stackoverflow
def flatten_list(l=[], limit=1000, counter=0):
    '''

    Converts a nested list into one combined list.

    :param l: a list object with (optionally) nested list.
    :param limit: the maximum amount of nested lists (recursive).
    :param counter:

    .. versionadded:: 0.1

    >>> l = [[['1'], [[2, 3, 4], [5, 6, [7]], [8]]], [9, 10, 11, 12], [13, 14]]
    >>> flatten_list(l)
    ['1', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    '''
    assert l
    assert type(l) == list
    assert limit > 0
    assert counter >= 0

    for i in xrange(len(l)):
        if (isinstance(l[i], (list, tuple)) and counter < limit):
            for a in l.pop(i):
                l.insert(i, a)
                i += 1
            counter += 1
            return flatten_list(l, limit, counter)
    return l


def cat_file(filename=None):
    '''

    Outputs the contents of a file.

    :param filename: the file to read from.
    :return: the contents of a file.
    :rtype: a string.

    .. versionadded:: 0.1

    >>> f = open('/tmp/test_cat_file', 'w')
    >>> f.write('This is a test case\\n.')
    >>> f.close()
    >>> cat_file('/tmp/test_cat_file')
    'This is a test case\\n.'

    '''
    assert filename
    assert type(filename) == str
    return open(filename).read()


def get_path(path=[]):
    '''

    Builds and normalizes a path.

    :param path: a list with the components of a path.
    :return: the full path.
    :rtype: a string.

    .. versionadded:: 0.1

    >>> p = ['/usr', 'share', 'logs/vars', 'included', 'hola.deb']
    >>> get_path(p)
    '/usr/share/logs/vars/included/hola.deb'

    '''
    assert path
    assert type(path) == list
    return os.path.normpath(os.path.realpath(
        os.path.abspath(os.path.join(*path))))


def package_to_path(package=None):
    '''

    Converts a python package string (e.g. "foo.bar") to a path string
    (e.g. "foo/bar").

    This function does not check if the python package really exists.

    :param package: a string containing the representation of a python package.
    :return: the path of the python package.
    :rtype: a string.

    .. versionadded:: 0.1

    >>> p = 'tribus.common.setup.utils'
    >>> package_to_path(p)
    'tribus/common/setup/utils'

    '''
    assert package
    assert type(package) == str
    return os.path.join(*package.split('.'))


def path_to_package(path=None):
    '''

    Converts a path string (e.g. "foo/bar") to a python package string
    (e.g. "foo.bar").

    This function does not check if the path contains a python package.

    :param path: a string containing a path.
    :return: a string with the representation of a python package.
    :rtype: a string.

    .. versionadded:: 0.1

    >>> p = 'tribus/common/setup/utils/'
    >>> path_to_package(p)
    'tribus.common.setup.utils'

    '''
    assert path
    assert type(path) == str
    return os.path.normpath(path).replace(os.sep, '.')


def list_files(path=None):
    '''

    Returns a list of all files in a directory (non-recursive).

    :param path: a string containing a path.
    :return: a list of all files in a directory (non-recursive).
    :rtype: a list.

    .. versionadded:: 0.1

    >>> import os
    >>> import shutil
    >>> from tribus.common.utils import list_files, get_path
    >>> tmpdir = get_path(['/tmp', 'test_list_files'])
    >>> tmpfiles = ['1.txt', '2.txt']
    >>> shutil.rmtree(tmpdir)
    >>> os.makedirs(tmpdir)
    >>> for t in tmpfiles:
    ...     f = open(get_path([tmpdir, t]), 'w')
    ...     f.write(t)
    ...     f.close()
    ... 
    >>> l = list_files(path=tmpdir)
    >>> l.sort()
    >>> l
    ['/tmp/test_list_files/1.txt', '/tmp/test_list_files/2.txt']

    '''
    assert path
    assert type(path) == str
    return [get_path([path, f]) for f in os.listdir(path) \
                                    if os.path.isfile(get_path([path, f]))]


def find_files(path=None, pattern='*.*'):
    '''

    Locate all the files matching the supplied filename pattern in and below the
    supplied root directory. If no pattern is supplied, all files will be
    returned.

    :param path: a string containing a path where the files will be looked for.
    :param pattern: a string containing a regular expression.
    :return: a list of files matching the pattern within path (recursive).
    :rtype: a list.

    .. versionadded:: 0.1

    >>> import os
    >>> import shutil
    >>> from tribus.common.utils import find_files, get_path
    >>> tmpdir_1 = get_path(['/tmp', 'test_find_files'])
    >>> tmpdir_2 = get_path([tmpdir_1, '2'])
    >>> tmpdir_3 = get_path([tmpdir_2, '3'])
    >>> tmpfiles = ['1.txt', '2.txt']
    >>> shutil.rmtree(tmpdir_1)
    >>> os.makedirs(tmpdir_3)
    >>> for t in tmpfiles:
    ...     f = open(get_path([tmpdir_2, t]), 'w')
    ...     f.write(t)
    ...     f.close()
    ...     for w in tmpfiles:
    ...         f = open(get_path([tmpdir_3, w]), 'w')
    ...         f.write(w)
    ...         f.close()
    ... 
    >>> l = find_files(path=tmpdir_1, pattern='*.*')
    >>> l.sort()
    >>> l
    ['/tmp/test_find_files/2/1.txt', '/tmp/test_find_files/2/2.txt', '/tmp/test_find_files/2/3/1.txt', '/tmp/test_find_files/2/3/2.txt']

    '''
    d = []
    assert path
    assert pattern
    assert type(path) == str
    assert type(pattern) == str
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for filename in fnmatch.filter(files, pattern):
            d.append(get_path([directory, filename]))
    return d


def list_dirs(path=None):
    '''

    Lists all subdirectories of a given path (non-recursive).

    :param path: a string containing a path.
    :return: a list of subdirectories under the given path (non-recursive).
    :rtype: a list.

    .. versionadded:: 0.1

    >>> import os
    >>> import shutil
    >>> from tribus.common.utils import list_dirs, get_path
    >>> tmpdir = get_path(['/tmp', 'test_list_dirs'])
    >>> tmpdirs_1 = ['uno', 'dos']
    >>> tmpdirs_2 = ['tres', 'cuatro']
    >>> shutil.rmtree(tmpdir)
    >>> os.makedirs(tmpdir)
    >>> for t in tmpdirs_1:
    ...     os.makedirs(get_path([tmpdir, t]))
    ... 
    >>> for w in tmpdirs_2:
    ...     os.makedirs(get_path([tmpdir, tmpdirs_1[0], w]))
    ... 
    >>> l = list_dirs(path=tmpdir)
    >>> l.sort()
    >>> l
    ['', 'dos', 'uno']

    '''
    assert path
    assert type(path) == str
    try:
        subdirectories = ['']+os.walk(os.path.normpath(path)).next()[1]
    except StopIteration:
        subdirectories = []
    return subdirectories


def find_dirs(path):
    """
    Get the subdirectories within a package
    This will include resources (non-submodules) and submodules
    """
    path = os.path.normpath(path)
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
