import copy
import os
import sys
import yaml

from tribus.common import serializer
from tribus.common.format import YAMLFormat
from tribus.common.schema import (SchemaError, KeyDict, Dict, String,
                                 Constant, OneOf, Int, Float)
from tribus.common.charms.errors import (
    ServiceConfigError, ServiceConfigValueError)

OPTION_SCHEMA = KeyDict({
        "type": OneOf(Constant("string"),
                      Constant("str"),  # Obsolete
                      Constant("int"),
                      Constant("boolean"),
                      Constant("float")),
        "default": OneOf(String(), Int(), Float()),
        "description": String(),
    },
    optional=["default", "description"],
    )

# Schema used to validate ConfigOptions specifications
CONFIG_SCHEMA = KeyDict({
    "options": Dict(String(), OPTION_SCHEMA),
    })

WARNED_STR_IS_OBSOLETE = False


class ConfigOptions(object):
    """Represents the configuration options exposed by a charm.

    The intended usage is that Charm provide access to these objects
    and then use them to `validate` inputs provided in the `juju
    set` and `juju deploy` code paths.
    """

    def __init__(self):
        self._data = {}

    def as_dict(self):
        return copy.deepcopy(self._data)

    def load(self, pathname):
        """Construct a ConfigOptions instance from a YAML file.

        If is currently allowed for `pathname` to be missing. An empty
        file with no allowable options will be assumed in that case.
        """
        data = None
        if os.path.exists(pathname):
            with open(pathname) as fh:
                data = fh.read()
        else:
            pathname = None
            data = "options: {}\n"

        if not data:
            raise ServiceConfigError(
                pathname, "Missing required service options metadata")
        self.parse(data, pathname)
        return self

    def parse(self, data, pathname=None):
        """Load data into the config object.

        Data can be a properly encoded YAML string or an dict, such as
        one returned by `get_serialization_data`.

        Each call to `parse` replaces any existing data.

        `data`: Python dict or YAML encoded dict containing a valid
        config options specification.
        `pathname`: optional pathname included in some errors
        """
        if isinstance(data, basestring):
            try:
                raw_data = serializer.yaml_load(data)
            except yaml.MarkedYAMLError, e:
                # Capture the path name on the error if present.
                if pathname is not None:
                    e.problem_mark = serializer.yaml_mark_with_path(
                        pathname, e.problem_mark)
                raise
        elif isinstance(data, dict):
            raw_data = data
        else:
            raise ServiceConfigError(
                pathname or "",
                "Unknown data type for config options: %s" % type(data))

        data = self.parse_serialization_data(raw_data, pathname)
        self._data = data
        # validate defaults
        self.get_defaults()

    def parse_serialization_data(self, data, pathname=None):
        """Verify we have sensible option metadata.

        Returns the `options` dict from within the YAML data.
        """
        if not data or not isinstance(data, dict):
            raise ServiceConfigError(
                pathname or "",
                "Expected YAML dict of options metadata")

        try:
            data = CONFIG_SCHEMA.coerce(data, [])
        except SchemaError, error:
            raise ServiceConfigError(
                pathname or "", "Invalid options specification: %s" % error)

        # XXX Drop this after everyone has migrated their config to 'string'.
        global WARNED_STR_IS_OBSOLETE
        if not WARNED_STR_IS_OBSOLETE:
            for name, info in data["options"].iteritems():
                for field, value in info.iteritems():
                    if field == "type" and value == "str":
                        sys.stderr.write(
                            "WARNING: Charm is using obsolete 'str' type "
                            "in config.yaml. Rename it to 'string'. %r \n" % (
                                pathname or ""))
                        WARNED_STR_IS_OBSOLETE = True
                        break

        return data["options"]

    def _validate_one(self, name, value):
        # see if there is a type associated with the option
        kind = self._data[name].get("type", "string")
        if kind not in validation_kinds:
            raise ServiceConfigValueError(
                "Unknown service option type: %s" % kind)

            # apply validation
        validator = validation_kinds[kind]
        value, valid = validator(value, self._data[name])

        if not valid:
            # Return value such that it roundtrips; this allows us to
            # report back the boolean false instead of the Python
            # output format, False
            raise ServiceConfigValueError(
                "Invalid value for %s: %s" % (
                    name, YAMLFormat().format_raw(value)))
        return value

    def get_defaults(self):
        """Return a mapping of option: default for all options."""
        d = {}
        for name, options in self._data.items():
            if "default" in options:
                d[name] = self._validate_one(name, options["default"])

        return d

    def validate(self, options):
        """Validate options using the loaded validation data.

        This method validates all the provided options, and returns a
        new dictionary with values properly typed.

        If a provided option is unknown or its value fails validation,
        ServiceConfigError is raised.
        """
        d = {}

        for option, value in options.items():
            if option not in self._data:
                raise ServiceConfigValueError(
                    "%s is not a valid configuration option." % (option))
            d[option] = self._validate_one(option, value)

        return d

    def get_serialization_data(self):
        return dict(options=self._data.copy())


# Validators return (type mapped value, valid boolean)
def validate_str(value, options):
    if isinstance(value, basestring):
        return value, True
    return value, False


def validate_int(value, options):
    try:
        return int(value), True
    except ValueError:
        return value, False


def validate_float(value, options):
    try:
        return float(value), True
    except ValueError:
        return value, False


def validate_boolean(value, options):
    if isinstance(value, bool):
        return value, True
    if value.lower() == "true":
        return True, True
    if value.lower() == "false":
        return False, True
    return value, False

# maps service option types to callables
validation_kinds = {
    "string": validate_str,
    "str": validate_str,  # Obsolete
    "int": validate_int,
    "float": validate_float,
    "boolean": validate_boolean,
    }
