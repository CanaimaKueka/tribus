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
import re
import urllib
import hashlib


# Taken from: http://stackoverflow.com/a/2158532
def flatten_list(l=[]):
    '''

    Converts a nested list into one combined list.

    :param l: a list object with (optionally) nested list.
    :returns: a generator with all nested lists combined.
    :rtype: a generator.

    .. versionadded:: 0.1

    >>> l = [[['1'], [[2, 3, 4], [5, 6, [7]], [8]]], [9, 10, 11, 12], [13, 14]]
    >>> list(flatten_list(l))
    ['1', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    >>> l = []
    >>> list(flatten_list(l))
    []

    '''
    from collections import Iterable
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, basestring):
            for sub in flatten_list(el):
                yield sub
        else:
            yield el


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

    Builds and normalizes a path. This will resolve symlinks to their
    destination and convert relative to absolute paths.

    This function does not check if the python path really exists.

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

    '''
    assert path
    assert type(path) == str
    return [get_path([path, f]) for f in os.listdir(path)
            if os.path.isfile(get_path([path, f]))]


def find_files(path=None, pattern='*'):
    '''

    Locate all the files matching the supplied filename pattern in and below
    the supplied root directory. If no pattern is supplied, all files will be
    returned.

    :param path: a string containing a path where the files will be looked for.
    :param pattern: a string containing a regular expression.
    :return: a list of files matching the pattern within path (recursive).
    :rtype: a list.

    .. versionadded:: 0.1

    '''
    d = []
    import fnmatch
    assert path
    assert pattern
    assert type(path) == str
    assert type(pattern) == str
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for filename in fnmatch.filter(files, pattern):
            if os.path.isfile(os.path.join(directory, filename)):
                if os.path.islink(os.path.join(directory, filename)):
                    d.append(os.path.join(get_path([directory]), filename))
                else:
                    d.append(get_path([directory, filename]))
    return d


def list_dirs(path=None):
    '''

    Lists all subdirectories of a given path (non-recursive).

    :param path: a string containing a path.
    :return: a list of subdirectories under the given path (non-recursive).
    :rtype: a list.

    .. versionadded:: 0.1

    '''
    assert path
    assert type(path) == str
    return [get_path([path, f]) for f in os.listdir(path)
            if os.path.isdir(get_path([path, f]))]


def find_dirs(path=None, pattern='*'):
    '''

    Locate all the directories matching the supplied pattern in and below
    the supplied root directory. If no pattern is supplied, all files will be
    returned.

    :param path: a string containing a path where the directories will be
                 looked for.
    :param pattern: a string containing a regular expression.
    :return: a list of directories matching the pattern
             within path (recursive).
    :rtype: a list.

    .. versionadded:: 0.1

    '''
    d = []
    import fnmatch
    assert path
    assert pattern
    assert type(path) == str
    assert type(pattern) == str
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for subdir in fnmatch.filter(subdirs, pattern):
            if os.path.isdir(os.path.join(directory, subdir)):
                if os.path.islink(os.path.join(directory, subdir)):
                    d.append(os.path.join(get_path([directory]), subdir))
                else:
                    d.append(get_path([directory, subdir]))
    return d


def list_items(path=None, dirs=True, files=True):
    '''

    Lists items under a given path (non-recursive, unnormalized).

    :param path: a string containing a path.
    :param dirs: if False, no directories will be included in the result.
    :param files: if False, no files will be included in the result.
    :return: a list of items under the given path (non-recursive).
    :rtype: a list.

    .. versionadded:: 0.1

    '''
    assert path
    assert type(path) == str
    return [f for f in os.listdir(path)
            if (os.path.isdir(os.path.join(path, f)) and dirs)
            or (os.path.isfile(os.path.join(path, f)) and files)]


def readconfig(filename, options=[], conffile=False, strip_comments=True):
    '''
    Reads a file whether if is a data or configuration file and returns
    its content in a dictionary or a list.

    :param filename: path to the file.

    :param options: a list of aditional options.

    :param conffile: if True then the result will be a dictionary else the result will be a list.

    :param strip_comments: if True then the comments in the file will be deleted.

    :return: a Dictionary or a List.

    :rtype: ``dict`` ``list``

    .. versionadded:: 0.1
    '''

    try:
        f = urllib.urlopen(filename) # No estoy seguro si esto sea una buena idea
    except:
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


def md5Checksum(filePath):
    '''
    Returns the md5sum from a file. Taken from:
    http://www.joelverhagen.com/blog/2011/02/md5-hash-of-file-in-python/

    :param filePath: path to the file from which its md5sum will be calculated.

    .. versionadded:: 0.1
    '''
    if os.path.exists(filePath):
        with open(filePath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()


def filename_generator(file_parts, new_m_time):
    filename = os.path.basename(file_parts[0])
    url = os.path.dirname(file_parts[0])
    ext = file_parts[1]
    m = hashlib.md5()
    m.update(filename)
    return '{0}/{1}.{2}{3}'.format(url, m.hexdigest(), new_m_time, ext)


def repeated_relation_counter(control_file):
    import deb822
    archivo = urllib.urlopen(control_file)
    for paragraph in deb822.Packages.iter_paragraphs(archivo):
        for rel_type, rel in paragraph.relations.items():
            if rel:
                for r in rel:
                    for rr in r:
                        encontrados = 0
                        for name in paragraph[rel_type].replace(',', ' ').split():
                            match = re.match('^'+rr['name'].replace("+", "\+").replace("-", "\-")+'$', name)
                            if match and rr.get('version'):
                                encontrados += 1
                        if encontrados > 2:
                            print paragraph['package'], encontrados
                            print r
