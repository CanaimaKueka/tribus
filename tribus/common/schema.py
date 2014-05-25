"""A schema system for validation of dict-based values."""
import re


class SchemaError(Exception):
    """Raised when invalid input is received."""

    def __init__(self, path, message):
        self.path = path
        self.message = message

        info = "%s: %s" % ("".join(self.path), self.message)
        super(Exception, self).__init__(info)


class SchemaExpectationError(SchemaError):
    """Raised when an expected value is not found."""

    def __init__(self, path, expected, got):
        self.expected = expected
        self.got = got
        message = "expected %s, got %s" % (expected, got)
        super(SchemaExpectationError, self).__init__(path, message)


class Constant(object):
    """Something that must be equal to a constant value."""

    def __init__(self, value):
        self.value = value

    def coerce(self, value, path):
        if value != self.value:
            raise SchemaExpectationError(path, repr(self.value), repr(value))
        return value


class Any(object):
    """Anything at all."""

    def coerce(self, value, path):
        return value


class OneOf(object):
    """Must necessarily match one of the given schemas."""

    def __init__(self, *schemas):
        """
        @param schemas: Any number of other schema objects.
        """
        self.schemas = schemas

    def coerce(self, value, path):
        """
        The result of the first schema which doesn't raise
        L{SchemaError} from its C{coerce} method will be returned.
        """
        best_error = None
        for i, schema in enumerate(self.schemas):
            try:
                return schema.coerce(value, path)
            except SchemaError, be:
                if not best_error or len(be.path) > len(best_error.path):
                    best_error = be

        raise best_error


class Bool(object):
    """Something that must be a C{bool}."""

    def coerce(self, value, path):
        if not isinstance(value, bool):
            raise SchemaExpectationError(path, "bool", repr(value))
        return value


class Int(object):
    """Something that must be an C{int} or C{long}."""

    def coerce(self, value, path):
        if not isinstance(value, (int, long)):
            raise SchemaExpectationError(path, "int", repr(value))
        return value


class Float(object):
    """Something that must be an C{int}, C{long}, or C{float}."""

    def coerce(self, value, path):
        if not isinstance(value, (int, long, float)):
            raise SchemaExpectationError(path, "number", repr(value))
        return value


class String(object):
    """Something that must be a C{str}."""

    def coerce(self, value, path):
        if not isinstance(value, str):
            raise SchemaExpectationError(path, "string", repr(value))
        return value


class Unicode(object):
    """Something that must be a C{unicode}."""

    def coerce(self, value, path):
        if not isinstance(value, unicode):
            raise SchemaExpectationError(path, "unicode", repr(value))
        return value


class Regex(object):
    """Something that must be a valid Python regular expression."""

    def coerce(self, value, path):
        try:
            regex = re.compile(value)
        except re.error:
            raise SchemaExpectationError(path,
                                         "regex",
                                         repr(value))
        return regex


class UnicodeOrString(object):
    """Something that must be a C{unicode} or {str}.

    If the value is a C{str}, it will automatically be decoded.
    """

    def __init__(self, encoding):
        """
        @param encoding: The encoding to automatically decode C{str}s with.
        """
        self.encoding = encoding

    def coerce(self, value, path):
        if isinstance(value, str):
            try:
                value = value.decode(self.encoding)
            except UnicodeDecodeError:
                raise SchemaExpectationError(
                    path, "unicode or %s string" % self.encoding,
                    repr(value))
        elif not isinstance(value, unicode):
            raise SchemaExpectationError(
                path, "unicode or %s string" % self.encoding,
                repr(value))
        return value


class List(object):
    """Something which must be a C{list}."""

    def __init__(self, schema):
        """
        @param schema: The schema that all values of the list must match.
        """
        self.schema = schema

    def coerce(self, value, path):
        if not isinstance(value, list):
            raise SchemaExpectationError(path, "list", repr(value))
        new_list = list(value)
        path.extend(["[", "?", "]"])
        try:
            for i, subvalue in enumerate(value):
                path[-2] = str(i)
                new_list[i] = self.schema.coerce(subvalue, path)
        finally:
            del path[-3:]
        return new_list


class Tuple(object):
    """Something which must be a fixed-length tuple."""

    def __init__(self, *schema):
        """
        @param schema: A sequence of schemas, which will be applied to
            each value in the tuple respectively.
        """
        self.schema = schema

    def coerce(self, value, path):
        if not isinstance(value, tuple):
            raise SchemaExpectationError(path, "tuple", repr(value))
        if len(value) != len(self.schema):
            raise SchemaExpectationError(
                path, "tuple with %d elements" % len(self.schema),
                repr(value))
        new_value = []
        path.extend(["[", "?", "]"])
        try:
            for i, (schema, value) in enumerate(zip(self.schema, value)):
                path[-2] = str(i)
                new_value.append(schema.coerce(value, path))
        finally:
            del path[-3:]
        return tuple(new_value)


class Dict(object):
    """Something which must be a C{dict} with arbitrary keys."""

    def __init__(self, key_schema, value_schema):
        """
        @param key_schema: The schema that keys must match.
        @param value_schema: The schema that values must match.
        """
        self.key_schema = key_schema
        self.value_schema = value_schema

    def coerce(self, value, path):
        if not isinstance(value, dict):
            raise SchemaExpectationError(path, "dict", repr(value))
        new_dict = {}
        key_path = path
        if not path:
            value_path = ["?"]
        else:
            value_path = path + [".", "?"]

        for key, subvalue in value.items():
            new_key = self.key_schema.coerce(key, key_path)
            try:
                value_path[-1] = str(key)
            except ValueError:
                value_path[-1] = repr(key)
            new_subvalue = self.value_schema.coerce(subvalue, value_path)
            new_dict[new_key] = new_subvalue
        return new_dict


class KeyDict(object):
    """Something which must be a C{dict} with defined keys.

    The keys must be constant and the values must match a per-key schema.
    """

    def __init__(self, schema, optional=None):
        """
        @param schema: A dict mapping keys to schemas that the values
            of those keys must match.
        """
        self.optional = set(optional or ())
        self.schema = schema

    def coerce(self, value, path):
        new_dict = {}
        if not isinstance(value, dict):
            raise SchemaExpectationError(path, "dict", repr(value))
        path = path[:]
        if path:
            path.append(".")
        path.append("?")
        for k, v in value.iteritems():
            if k in self.schema:
                try:
                    path[-1] = str(k)
                except ValueError:
                    path[-1] = repr(k)
                new_dict[k] = self.schema[k].coerce(v, path)
            else:
                # Just preserve entries which are not in the schema.
                # This is less likely to eat important values due to
                # different app versions being used, for instance.
                new_dict[k] = v

        for k in self.schema:
            if k not in value and k not in self.optional:
                path[-1] = k
                raise SchemaError(path, "required value not found")

        # No need to restore path.  It was copied.
        return new_dict


class SelectDict(object):
    """Something that must be a C{dict} whose schema depends on some value."""

    def __init__(self, key, schemas):
        """
        @param key: a key we expect to be in each of the possible schemas,
            which we use to select which schema to coerce to.

        @param schemas: a dictionary mapping values for C{key} to schemas,
            to which the eventual value should be coerced.
        """
        self.key = key
        self.schemas = schemas

    def coerce(self, value, path):
        if self.key not in value:
            raise SchemaError(
                path + ['.', self.key], "required value not found")
        selected = value[self.key]
        return self.schemas[selected].coerce(value, path)


class OAuthString(String):
    """A L{String} containing OAuth information, colon-separated.

    The string should contain three parts::

      consumer-key:resource-key:resource-secret

    Each part is stripped of leading and trailing whitespace.

    @return: A 3-tuple of C{consumer-key}, C{resource-key},
        C{resource-secret}.
    """

    def coerce(self, value, path):
        value = super(OAuthString, self).coerce(value, path)
        parts = tuple(part.strip() for part in value.split(":"))
        if len(parts) != 3:
            raise SchemaError(
                path, "does not contain three colon-separated parts")
        if "" in parts:
            raise SchemaError(
                path, "one or more parts are empty")
        return parts
