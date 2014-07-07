# # -*- encoding: utf-8 -*-

# import os
# import yaml
# import inspect

# from juju.charm import tests
# from juju.charm.metadata import (
#     MetaData, MetaDataError, InterfaceExpander, SchemaError)
# from juju.errors import FileNotFound
# from juju.lib.testing import TestCase
# from juju.lib import serializer

# test_repository_path = os.path.join(
#     os.path.dirname(inspect.getabsfile(tests)),
#     "repository")
# sample_path = os.path.join(
#     test_repository_path, "series", "dummy", "metadata.yaml")
# sample_configuration = open(sample_path).read()


# class MetaDataTest(TestCase):

#     def setUp(self):
#         self.metadata = MetaData()
#         self.sample = sample_configuration

#     def change_sample(self):
#         """Return a context manager for hacking the sample data.

#         This should be used follows:

#             with self.change_sample() as data:
#                 data["some-key"] = "some-data"

#         The changed sample file content will be available in self.sample
#         once the context is done executing.
#         """

#         class HackManager(object):

#             def __enter__(mgr):
#                 mgr.data = serializer.yaml_load(self.sample)
#                 return mgr.data

#             def __exit__(mgr, exc_type, exc_val, exc_tb):
#                 self.sample = serializer.yaml_dump(mgr.data)
#                 return False
#         return HackManager()

#     def test_path_argument_loads_charm_info(self):
#         info = MetaData(sample_path)
#         self.assertEquals(info.name, "dummy")

#     def test_check_basic_info_before_loading(self):
#         """
#         Attributes should be set to None before anything is loaded.
#         """
#         self.assertEquals(self.metadata.name, None)
#         self.assertEquals(self.metadata.obsolete_revision, None)
#         self.assertEquals(self.metadata.summary, None)
#         self.assertEquals(self.metadata.description, None)
#         self.assertEquals(self.metadata.is_subordinate, False)
#         self.assertEquals(self.metadata.format, 1)

#     def test_parse_and_check_basic_info(self):
#         """
#         Parsing the content file should work. :-)  Basic information will
#         be available as attributes of the info file.
#         """
#         self.metadata.parse(self.sample)
#         self.assertEquals(self.metadata.name, "dummy")
#         self.assertEquals(self.metadata.obsolete_revision, None)
#         self.assertEquals(self.metadata.summary, u"That's a dummy charm.")
#         self.assertEquals(self.metadata.description,
#                           u"This is a longer description which\n"
#                           u"potentially contains multiple lines.\n")
#         self.assertEquals(self.metadata.is_subordinate, False)

#     def test_is_subordinate(self):
#         """Validate rules for detecting proper subordinate charms are working"""
#         logging_path = os.path.join(
#             test_repository_path, "series", "logging", "metadata.yaml")
#         logging_configuration = open(logging_path).read()
#         self.metadata.parse(logging_configuration)
#         self.assertTrue(self.metadata.is_subordinate)

#     def test_subordinate_without_container_relation(self):
#         """Validate rules for detecting proper subordinate charms are working

#         Case where no container relation is specified.
#         """
#         with self.change_sample() as data:
#             data["subordinate"] = True

#         error = self.assertRaises(MetaDataError, self.metadata.parse, self.sample, "some/path")
#         self.assertIn("some/path labeled subordinate but lacking scope:container `requires` relation",
#                       str(error))

#     def test_scope_constraint(self):
#         """Verify the scope constrain is parsed properly."""
#         logging_path = os.path.join(
#             test_repository_path, "series", "logging", "metadata.yaml")
#         logging_configuration = open(logging_path).read()
#         self.metadata.parse(logging_configuration)
#         # Verify the scope settings
#         self.assertEqual(self.metadata.provides[u"logging-client"]["scope"],
#                          "global")
#         self.assertEqual(self.metadata.requires[u"logging-directory"]["scope"],
#                          "container")
#         self.assertTrue(self.metadata.is_subordinate)

#     def assert_parse_with_revision(self, with_path):
#         """
#         Parsing the content file should work. :-)  Basic information will
#         be available as attributes of the info file.
#         """
#         with self.change_sample() as data:
#             data["revision"] = 123
#         log = self.capture_logging("juju.charm")
#         self.metadata.parse(self.sample, "some/path" if with_path else None)
#         if with_path:
#             self.assertIn(
#                 "some/path: revision field is obsolete. Move it to the "
#                 "'revision' file.",
#                 log.getvalue())
#         self.assertEquals(self.metadata.name, "dummy")
#         self.assertEquals(self.metadata.obsolete_revision, 123)
#         self.assertEquals(self.metadata.summary, u"That's a dummy charm.")
#         self.assertEquals(self.metadata.description,
#                           u"This is a longer description which\n"
#                           u"potentially contains multiple lines.\n")
#         self.assertEquals(
#             self.metadata.get_serialization_data()["revision"], 123)

#     def test_parse_with_revision(self):
#         self.assert_parse_with_revision(True)
#         self.assert_parse_with_revision(False)

#     def test_load_calls_parse_calls_parse_serialzation_data(self):
#         """
#         We'll break the rules a little bit here and test the implementation
#         itself just so that we don't have to test *everything* twice. If
#         load() calls parse() which calls parse_serialzation_data(), then
#         whatever happens with parse_serialization_data(), happens with the
#         others.
#         """
#         serialization_data = {"Hi": "there!"}
#         yaml_data = serializer.yaml_dump(serialization_data)
#         path = self.makeFile(yaml_data)
#         mock = self.mocker.patch(self.metadata)
#         mock.parse(yaml_data, path)
#         self.mocker.passthrough()
#         mock.parse_serialization_data(serialization_data, path)
#         self.mocker.replay()

#         self.metadata.load(path)
#         # Do your magic Mocker!

#     def test_metadata_parse_error_includes_path_with_load(self):
#         broken = ("""\
#         description: helo
# name: hi
# requires: {interface: zebra
# revision: 0
# summary: hola""")

#         path = self.makeFile()
#         e = self.assertRaises(
#             yaml.YAMLError, self.metadata.parse, broken, path)
#         self.assertIn(path, str(e))

#     def test_schema_error_includes_path_with_load(self):
#         """
#         When using load(), the exception message should mention the
#         path name which was attempted.
#         """
#         with self.change_sample() as data:
#             data["revision"] = "1"
#         filename = self.makeFile(self.sample)
#         error = self.assertRaises(MetaDataError,
#                                   self.metadata.load, filename)
#         self.assertEquals(str(error),
#                           "Bad data in charm info: %s: revision: "
#                           "expected int, got '1'" % filename)

#     def test_load_missing_file(self):
#         """
#         When using load(), the exception message should mention the
#         path name which was attempted.
#         """
#         filename = self.makeFile()
#         error = self.assertRaises(FileNotFound,
#                                   self.metadata.load, filename)
#         self.assertEquals(error.path, filename)

#     def test_name_summary_and_description_are_utf8(self):
#         """
#         Textual fields are decoded to unicode by the schema using UTF-8.
#         """
#         value = u"áéíóú"
#         str_value = value.encode("utf-8")
#         with self.change_sample() as data:
#             data["name"] = str_value
#             data["summary"] = str_value
#             data["description"] = str_value
#         self.metadata.parse(self.sample)
#         self.assertEquals(self.metadata.name, value)
#         self.assertEquals(self.metadata.summary, value)
#         self.assertEquals(self.metadata.description, value)

#     def test_get_serialized_data(self):
#         """
#         The get_serialization_data() function should return an object which
#         may be passed to parse_serialization_data() to restore the state of
#         the instance.
#         """
#         self.metadata.parse(self.sample)
#         serialization_data = self.metadata.get_serialization_data()
#         self.assertEquals(serialization_data["name"], "dummy")

#     def test_provide_implicit_relation(self):
#         """Verify providing a juju-* reserved relation errors"""
#         with self.change_sample() as data:
#             data["provides"] = {"juju-foo": {"interface": "juju-magic", "scope": "container"}}

#         # verify relation level error
#         error = self.assertRaises(MetaDataError,
#                                   self.metadata.parse, self.sample)
#         self.assertIn("Charm dummy attempting to provide relation in implicit relation namespace: juju-foo",
#                       str(error))

#         # verify interface level error
#         with self.change_sample() as data:
#             data["provides"] = {"foo-rel": {"interface": "juju-magic", "scope": "container"}}

#         error = self.assertRaises(MetaDataError,
#                                   self.metadata.parse, self.sample)
#         self.assertIn(
#             "Charm dummy attempting to provide interface in implicit namespace: juju-magic (relation: foo-rel)",
#             str(error))

#     def test_format(self):
#         # Defaults to 1
#         self.metadata.parse(self.sample)
#         self.assertEquals(self.metadata.format, 1)

#         # Explicitly set to 1
#         with self.change_sample() as data:
#             data["format"] = 1
#         self.metadata.parse(self.sample)
#         self.assertEquals(self.metadata.format, 1)

#         # Explicitly set to 2
#         with self.change_sample() as data:
#             data["format"] = 2
#         self.metadata.parse(self.sample)
#         self.assertEquals(self.metadata.format, 2)

#         # Explicitly set to 3; however this is an unknown format for Juju
#         with self.change_sample() as data:
#             data["format"] = 3
#         error = self.assertRaises(MetaDataError, self.metadata.parse, self.sample)
#         self.assertIn("Charm dummy uses an unknown format: 3", str(error))


# class ParseTest(TestCase):
#     """Test the parsing of some well-known sample files"""

#     def get_metadata(self, charm_name):
#         """Get the associated metadata for a given charm, eg ``wordpress``"""
#         metadata = MetaData(os.path.join(
#             test_repository_path, "series", charm_name, "metadata.yaml"))
#         self.assertEqual(metadata.name, charm_name)
#         return metadata

#     def test_mysql_sample(self):
#         """Test parse of a relation written in shorthand format.

#         Such relations are defined as follows::
#            provides:
#              server: mysql
#         """
#         metadata = self.get_metadata("mysql")
#         self.assertEqual(metadata.peers, None)
#         self.assertEqual(
#             metadata.provides["server"],
#             {"interface": "mysql", "limit": None, "optional": False, "scope": "global"})
#         self.assertEqual(metadata.requires, None)

#     def test_riak_sample(self):
#         """Test multiple interfaces defined in long form, with defaults."""
#         metadata = self.get_metadata("riak")
#         self.assertEqual(
#             metadata.peers["ring"],
#             {"interface": "riak", "limit": 1, "optional": False, "scope": "global"})
#         self.assertEqual(
#             metadata.provides["endpoint"],
#             {"interface": "http", "limit": None, "optional": False, "scope": "global"})
#         self.assertEqual(
#             metadata.provides["admin"],
#             {"interface": "http", "limit": None, "optional": False, "scope": "global"})
#         self.assertEqual(metadata.requires, None)

#     def test_wordpress_sample(self):
#         """Test multiple interfaces defined in long form, without defaults."""
#         metadata = self.get_metadata("wordpress")
#         self.assertEqual(metadata.peers, None)
#         self.assertEqual(
#             metadata.provides["url"],
#             {"interface": "http", "limit": None, "optional": False, "scope": "global"})
#         self.assertEqual(
#             metadata.requires["db"],
#             {"interface": "mysql", "limit": 1, "optional": False, "scope": "global"})
#         self.assertEqual(
#             metadata.requires["cache"],
#             {"interface": "varnish", "limit": 2, "optional": True, "scope": "global"})

#     def test_interface_expander(self):
#         """Test rewriting of a given interface specification into long form.

#         InterfaceExpander uses `coerce` to do one of two things:

#           - Rewrite shorthand to the long form used for actual storage
#           - Fills in defaults, including a configurable `limit`

#         This test ensures test coverage on each of these branches, along
#         with ensuring the conversion object properly raises SchemaError
#         exceptions on invalid data.
#         """
#         expander = InterfaceExpander(limit=None)

#         # shorthand is properly rewritten
#         self.assertEqual(
#             expander.coerce("http", ["provides"]),
#             {"interface": "http", "limit": None, "optional": False, "scope": "global"})

#         # defaults are properly applied
#         self.assertEqual(
#             expander.coerce(
#                 {"interface": "http"}, ["provides"]),
#             {"interface": "http", "limit": None, "optional": False, "scope": "global"})
#         self.assertEqual(
#             expander.coerce(
#                 {"interface": "http", "limit": 2}, ["provides"]),
#             {"interface": "http", "limit": 2, "optional": False, "scope": "global"})
#         self.assertEqual(
#             expander.coerce(
#                 {"interface": "http", "optional": True, "scope": "global"},
#                 ["provides"]),
#             {"interface": "http", "limit": None, "optional": True, "scope": "global"})

#         # invalid data raises SchemaError
#         self.assertRaises(
#             SchemaError,
#             expander.coerce, 42, ["provides"])
#         self.assertRaises(
#             SchemaError,
#             expander.coerce,
#             {"interface": "http", "optional": None, "scope": "global"}, ["provides"])
#         self.assertRaises(
#             SchemaError,
#             expander.coerce,
#             {"interface": "http", "limit": "none, really"}, ["provides"])

#         # can change `limit` default
#         expander = InterfaceExpander(limit=1)
#         self.assertEqual(
#             expander.coerce("http", ["consumes"]),
#             {"interface": "http", "limit": 1, "optional": False, "scope": "global"})
