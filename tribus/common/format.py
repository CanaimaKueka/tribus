"""Utility functions and constants to support uniform i/o formatting."""

import json
import os

import yaml

from tribus.common.errors import jujuError


class BaseFormat(object):
    """Maintains parallel code paths for input and output formatting
    through the subclasses PythonFormat (Python str formatting with JSON
    encoding) and YAMLFormat.
    """

    def parse_keyvalue_pairs(self, pairs):
        """Parses key value pairs, using `_parse_value` for specific format"""
        data = {}
        for kv in pairs:
            if "=" not in kv:
                raise JujuError(
                    "Expected `option=value`. Found `%s`" % kv)

            k, v = kv.split("=", 1)
            if v.startswith("@"):
                # Handle file input, any parsing/sanitization is done next
                # with respect to charm format
                filename = v[1:]
                try:
                    with open(filename, "r") as f:
                        v = f.read()
                except IOError:
                    raise JujuError(
                        "No such file or directory: %s (argument:%s)" % (
                            filename,
                            k))
                except Exception, e:
                    raise JujuError("Bad file %s" % e)

            data[k] = self._parse_value(k, v)

        return data

    def _parse_value(self, key, value):
        """Interprets value as a str"""
        return value

    def should_delete(self, value):
        """Whether `value` implies corresponding key should be deleted"""
        return not value.strip()


class PythonFormat(BaseFormat):
    """Supports backwards compatibility through str and JSON encoding."""

    charm_format = 1

    def format(self, data):
        """Formats `data` using Python str encoding"""
        return str(data)

    def format_raw(self, data):
        """Add extra \n seen in Python format, so not truly raw"""
        return self.format(data) + "\n"

    # For the old format: 1, using JSON serialization introduces some
    # subtle issues around Unicode conversion that then later results
    # in bugginess. For compatibility reasons, we keep these old bugs
    # around, by dumping and loading into JSON at appropriate points.

    def dump(self, data):
        """Dumps using JSON serialization"""
        return json.dumps(data)

    def load(self, data):
        """Loads data, but also converts str to Unicode"""
        return json.loads(data)


class YAMLFormat(BaseFormat):
    """New format that uses YAML, so no unexpected encoding issues"""

    charm_format = 2

    def format(self, data):
        """Formats `data` in Juju's preferred YAML format"""
        # Return value such that it roundtrips; this allows us to
        # report back the boolean false instead of the Python
        # output format, False
        if data is None:
            return ""
        serialized = yaml.dump(
            data, indent=4, default_flow_style=False, width=80,
            allow_unicode=True, Dumper=yaml.CSafeDumper)
        if serialized.endswith("\n...\n"):
            # Remove explicit doc end sentinel, still valid yaml
            serialized = serialized[0:-5]
        # Also remove any extra \n, will still be valid yaml
        return serialized.rstrip("\n")

    def format_raw(self, data):
        """Formats `data` as a raw string if str, otherwise as YAML"""
        if isinstance(data, str):
            return data
        else:
            return self.format(data)

    # Use the same format for dump
    dump = format

    def load(self, data):
        """Loads data safely, ensuring no Python specific type info leaks"""
        return yaml.load(data, Loader=yaml.CSafeLoader)


def is_valid_charm_format(charm_format):
    """True if `charm_format` is a valid format"""
    return charm_format in (PythonFormat.charm_format, YAMLFormat.charm_format)


def get_charm_formatter(charm_format):
    """Map `charm_format` to the implementing strategy for that format"""
    if charm_format == PythonFormat.charm_format:
        return PythonFormat()
    elif charm_format == YAMLFormat.charm_format:
        return YAMLFormat()
    else:
        raise JujuError(
            "Expected charm format to be either 1 or 2, got %s" % (
                charm_format,))


def get_charm_formatter_from_env():
    """Return the formatter specified by $_JUJU_CHARM_FORMAT"""
    return get_charm_formatter(int(
            os.environ.get("_JUJU_CHARM_FORMAT", "1")))
