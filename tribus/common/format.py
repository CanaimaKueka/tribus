#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
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

"""

Utility functions and constants to support uniform I/O formatting.

"""

import json
import os
import yaml

from tribus.common.errors import TribusError


class BaseFormat(object):

    """

    A generic file format class.

    Maintains parallel code paths for input and output formatting
    through the subclasses PythonFormat (Python str formatting with JSON
    encoding) and YAMLFormat.

    """

    def parse_keyvalue_pairs(self, pairs):
        """

        Parse key value pairs, using ``_parse_value`` for specific format.

        :param pairs:
        :return:

        """
        data = {}
        for kv in pairs:
            if '=' not in kv:
                raise TribusError('Expected "option=value". Found "%s"' % kv)

            k, v = kv.split('=', 1)
            if v.startswith('@'):
                # Handle file input, any parsing/sanitization is done next
                # with respect to charm format
                filename = v[1:]
                try:
                    with open(filename, 'r') as f:
                        v = f.read()
                except IOError:
                    raise TribusError('No such file or directory: '
                                      '%s (argument:%s)' % (filename, k))
                except Exception, e:
                    raise TribusError('Bad file %s' % e)

            data[k] = self._parse_value(k, v)

        return data

    def _parse_value(self, key, value):
        """Interpret value as a str."""
        return value

    def should_delete(self, value):
        """Whether ``value`` implies corresponding key should be deleted."""
        return not value.strip()


class PythonFormat(BaseFormat):

    """Supports backwards compatibility through str and JSON encoding."""

    charm_format = 1

    def format(self, data):
        """Format ``data`` using Python str encoding."""
        return str(data)

    def format_raw(self, data):
        """Add extra carrier return seen in Python format, so not truly raw."""
        return self.format(data) + '\n'

    # For the old format: 1, using JSON serialization introduces some
    # subtle issues around Unicode conversion that then later results
    # in bugginess. For compatibility reasons, we keep these old bugs
    # around, by dumping and loading into JSON at appropriate points.

    def dump(self, data):
        """Dump using JSON serialization."""
        return json.dumps(data)

    def load(self, data):
        """Load data, but also converts ``str`` to ``unicode``."""
        return json.loads(data)


class YAMLFormat(BaseFormat):

    """New format that uses YAML, so no unexpected encoding issues."""

    charm_format = 2

    def format(self, data):
        """Format ``data`` in Tribus preferred YAML format."""
        # Return value such that it roundtrips; this allows us to
        # report back the boolean false instead of the Python
        # output format, False
        if data is None:
            return ''
        serialized = yaml.dump(data=data, indent=4, default_flow_style=False,
                               width=80, allow_unicode=True,
                               Dumper=yaml.CSafeDumper)
        if serialized.endswith('\n...\n'):
            # Remove explicit doc end sentinel, still valid yaml
            serialized = serialized[0:-5]
        # Also remove any extra \n, will still be valid yaml
        return serialized.rstrip('\n')

    def format_raw(self, data):
        """Format ``data`` as a raw string if str, otherwise as YAML."""
        if isinstance(data, str):
            return data
        else:
            return self.format(data)

    # Use the same format for dump
    dump = format

    def load(self, data):
        """Load data safely, ensuring no Python specific type info leaks."""
        return yaml.load(stream=data, Loader=yaml.CSafeLoader)


def is_valid_charm_format(charm_format):
    """True if `charm_format` is a valid format."""
    return charm_format in (PythonFormat.charm_format, YAMLFormat.charm_format)


def get_charm_formatter(charm_format):
    """Map ``charm_format`` to the implementing strategy for that format."""
    if charm_format == PythonFormat.charm_format:
        return PythonFormat()
    elif charm_format == YAMLFormat.charm_format:
        return YAMLFormat()
    else:
        raise TribusError('Expected charm format to be either 1 or 2, got %s' %
                          (charm_format,))


def get_charm_formatter_from_env():
    """Return the formatter specified by ${TRIBUS_CHARM_FORMAT}."""
    return get_charm_formatter(int(os.environ.get('TRIBUS_CHARM_FORMAT', '1')))
