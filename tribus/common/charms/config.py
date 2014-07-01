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

"""Contains a representation of the configuration of a charm."""

import copy
import os
import sys
import yaml

from tribus.common import serializer
from tribus.common.format import YAMLFormat
from tribus.common.schema import (SchemaError, KeyDict, Dict, String,
                                  Constant, OneOf, Int, Float)
from tribus.common.charms.errors import (ServiceConfigError,
                                         ServiceConfigValueError)

OPTION_SCHEMA = KeyDict({'type': OneOf(Constant('string'),
                                       Constant('str'),
                                       Constant('int'),
                                       Constant('boolean'),
                                       Constant('float')),
                         'default': OneOf(String(), Int(), Float()),
                         'description': String()},
                        optional=['default', 'description'])

CONFIG_SCHEMA = KeyDict({'options': Dict(String(), OPTION_SCHEMA)})

WARNED_STR_IS_OBSOLETE = False


class ConfigOptions(object):

    """

    Represents the configuration options exposed by a charm.

    The intended usage is that Charm provide access to these objects
    and then use them to `validate` inputs.

    """

    def __init__(self):
        """Initialize data dict."""
        self._data = {}

    def as_dict(self):
        """Make a deepcopy of the data dict."""
        return copy.deepcopy(self._data)

    def load(self, pathname):
        """

        Construct a ConfigOptions instance from a YAML file.

        If is currently allowed for `pathname` to be missing. An empty
        file with no allowable options will be assumed in that case.

        :param pathname: the pathname to the `config.yaml` file.
        :return: a `ConfigOptions` instance.

        """
        data = None

        if os.path.exists(pathname):
            with open(pathname) as fh:
                data = fh.read()
        else:
            pathname = None
            data = "options: {}\n"

        if not data:
            raise ServiceConfigError(pathname, ('Missing required service '
                                                'options metadata.'))
        self.parse(data, pathname)

        return self

    def parse(self, data, pathname=None):
        """

        Load data into the config object.

        Data can be a properly encoded YAML string or a dict, such as
        one returned by `get_serialization_data`.

        Each call to `parse` replaces any existing data.

        :param data: Python dict or YAML encoded dict containing a valid
                     config options specification.
        :param pathname: optional pathname included in some errors.

        """
        if isinstance(data, basestring):
            try:
                raw_data = serializer.yaml_load(data)
            except yaml.MarkedYAMLError, e:
                if pathname is not None:
                    e.problem_mark = serializer.yaml_mark_with_path(
                        pathname, e.problem_mark)
                raise

        elif isinstance(data, dict):
            raw_data = data
        else:
            raise ServiceConfigError(pathname or '', ('Unknown data type for '
                                                      'config options: '
                                                      '%s' % type(data)))

        self._data = self.parse_serialization_data(raw_data, pathname)
        self.get_defaults()

    def parse_serialization_data(self, data, pathname=None):
        """

        Verify we have sensible option metadata.

        Returns the `options` dict from within the YAML data.

        """
        if not data or not isinstance(data, dict):
            raise ServiceConfigError(pathname or '', ('Expected YAML dict of '
                                                      'options metadata.'))

        try:
            data = CONFIG_SCHEMA.coerce(data, [])
        except SchemaError, error:
            raise ServiceConfigError(pathname or '', ('Invalid options '
                                                      'specification: '
                                                      '%s' % error))

        global WARNED_STR_IS_OBSOLETE
        if not WARNED_STR_IS_OBSOLETE:
            for name, info in data['options'].iteritems():
                for field, value in info.iteritems():
                    if field == 'type' and value == 'str':
                        sys.stderr.write(('WARNING: Charm is using obsolete '
                                          '"str" type in config.yaml. Rename '
                                          'it to "string". %r '
                                          '\n' % (pathname or '')))
                        WARNED_STR_IS_OBSOLETE = True
                        break

        return data['options']

    def _validate_one(self, name, value):
        """Validate config options."""
        # see if there is a type associated with the option
        kind = self._data[name].get('type', 'string')

        if kind not in validation_kinds:
            raise ServiceConfigValueError('Unknown service option type: '
                                          '%s' % kind)

        # apply validation
        validator = validation_kinds[kind]
        value, valid = validator(value, self._data[name])

        if not valid:
            # Return value such that it roundtrips; this allows us to
            # report back the boolean false instead of the Python
            # output format, False
            raise ServiceConfigValueError(
                'Invalid value for %s: %s' % (name,
                                              YAMLFormat().format_raw(value)))
        return value

    def get_defaults(self):
        """Return a mapping of option: default for all options."""
        d = {}
        for name, options in self._data.items():
            if 'default' in options:
                d[name] = self._validate_one(name, options['default'])

        return d

    def validate(self, options):
        """

        Validate options using the loaded validation data.

        This method validates all the provided options, and returns a
        new dictionary with values properly typed.

        If a provided option is unknown or its value fails validation,
        ServiceConfigError is raised.

        """
        d = {}

        for option, value in options.items():
            if option not in self._data:
                raise ServiceConfigValueError(
                    '%s is not a valid configuration option.' % (option))
            d[option] = self._validate_one(option, value)

        return d

    def get_serialization_data(self):
        """Return the data dict."""
        return dict(options=self._data.copy())


# Validators return (type mapped value, valid boolean)
def validate_str(value, options):
    """Validate a string."""
    if isinstance(value, basestring):
        return value, True
    return value, False


def validate_int(value, options):
    """Validate a int."""
    try:
        return int(value), True
    except ValueError:
        return value, False


def validate_float(value, options):
    """Validate a float."""
    try:
        return float(value), True
    except ValueError:
        return value, False


def validate_boolean(value, options):
    """Validate a boolean."""
    if isinstance(value, bool):
        return value, True
    if value.lower() == 'true':
        return True, True
    if value.lower() == 'false':
        return False, True
    return value, False

# maps service option types to callables
validation_kinds = {'string': validate_str,
                    'str': validate_str,
                    'int': validate_int,
                    'float': validate_float,
                    'boolean': validate_boolean}
