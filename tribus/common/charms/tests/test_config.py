# from StringIO import StringIO
# import sys

# import yaml

# from juju.lib import serializer
# from juju.lib.testing import TestCase
# from juju.charm.config import ConfigOptions
# from juju.charm.errors import ServiceConfigError, ServiceConfigValueError

# sample_configuration = """
# options:
#   title:
#     default: My Title
#     description: A descriptive title used for the service.
#     type: string
#   outlook:
#     description: No default outlook.
#     type: string
#   username:
#     default: admin001
#     description: The name of the initial account (given admin permissions).
#     type: string
#   skill-level:
#     description: A number indicating skill.
#     type: int
# """

# sample_yaml_data = serializer.yaml_load(sample_configuration)

# sample_config_defaults = {"title": "My Title",
#                           "username": "admin001"}


# class ConfigOptionsTest(TestCase):

#     def setUp(self):
#         self.config = ConfigOptions()

#     def test_load(self):
#         """Validate we can load data or get expected errors."""

#         # load valid data
#         filename = self.makeFile(sample_configuration)
#         self.config.load(filename)
#         self.assertEqual(self.config.get_serialization_data(),
#                          sample_yaml_data)

#         # test with dict based data
#         self.config.parse(sample_yaml_data)
#         self.assertEqual(self.config.get_serialization_data(),
#                          sample_yaml_data)

#         # and with an unhandled type
#         self.assertRaises(TypeError, self.config.load, 1.234)

#     def test_load_file(self):
#         sample_path = self.makeFile(sample_configuration)
#         config = ConfigOptions()
#         config.load(sample_path)

#         self.assertEqual(config.get_serialization_data(),
#                          sample_yaml_data)

#         # and an expected exception
#         # on an empty file
#         empty_file = self.makeFile("")
#         error = self.assertRaises(ServiceConfigError, config.load, empty_file)
#         self.assertEqual(
#             str(error),
#             ("Error processing %r: "
#              "Missing required service options metadata") % empty_file)

#         # a missing filename is allowed
#         config = config.load("missing_file")

#     def test_defaults(self):
#         self.config.parse(sample_configuration)
#         defaults = self.config.get_defaults()
#         self.assertEqual(defaults, sample_config_defaults)

#     def test_defaults_validated(self):
#         e = self.assertRaises(
#             ServiceConfigValueError,
#             self.config.parse,
#             serializer.yaml_dump(
#                 {"options": {
#                     "foobar": {
#                         "description": "beyond what?",
#                         "type": "string",
#                         "default": True}}}))
#         self.assertEqual(
#             str(e), "Invalid value for foobar: true")

#     def test_as_dict(self):
#         # load valid data
#         filename = self.makeFile(sample_configuration)
#         self.config.load(filename)

#         # Verify dictionary serialization
#         schema_dict = self.config.as_dict()
#         self.assertEqual(
#             schema_dict,
#             serializer.yaml_load(sample_configuration)["options"])

#         # Verify the dictionary is a copy
#         # Poke at embedded objects
#         schema_dict["outlook"]["default"] = 1
#         schema2_dict = self.config.as_dict()
#         self.assertFalse("default" in schema2_dict["outlook"])

#     def test_parse(self):
#         """Verify that parse checks and raises."""
#         # no options dict
#         self.assertRaises(
#             ServiceConfigError, self.config.parse, {"foo": "bar"})

#         # and with bad data expected exceptions
#         error = self.assertRaises(yaml.YAMLError,
#                           self.config.parse, "foo: [1, 2", "/tmp/zamboni")
#         self.assertIn("/tmp/zamboni", str(error))

#     def test_validate(self):
#         sample_input = {"title": "Helpful Title", "outlook": "Peachy"}

#         self.config.parse(sample_configuration)
#         data = self.config.validate(sample_input)

#         # This should include an overridden value, a default and a new value.
#         self.assertEqual(data,
#                          {"outlook": "Peachy",
#                           "title": "Helpful Title"})

#         # now try to set a value outside the expected
#         sample_input["bad"] = "value"
#         error = self.assertRaises(ServiceConfigValueError,
#                                   self.config.validate, sample_input)
#         self.assertEqual(error.message,
#                          "bad is not a valid configuration option.")

#         # validating with an empty instance
#         # the service takes no options
#         config = ConfigOptions()
#         self.assertRaises(
#             ServiceConfigValueError, config.validate, sample_input)

#     def test_validate_float(self):
#         self.config.parse(serializer.yaml_dump(
#             {"options": {
#                 "score": {
#                     "description": "A number indicating score.",
#                     "type": "float"}}}))
#         error = self.assertRaises(ServiceConfigValueError,
#                                   self.config.validate, {"score": "arg"})
#         self.assertEquals(str(error), "Invalid value for score: arg")

#         data = self.config.validate({"score": "82.1"})
#         self.assertEqual(data, {"score": 82.1})

#     def test_validate_string(self):
#         self.config.parse(sample_configuration)

#         error = self.assertRaises(ServiceConfigValueError,
#                                   self.config.validate, {"title": True})
#         self.assertEquals(str(error), "Invalid value for title: true")

#         data = self.config.validate({"title": u"Good"})
#         self.assertEqual(data, {"title": u"Good"})

#     def test_validate_boolean(self):
#         self.config.parse(serializer.yaml_dump(
#             {"options": {
#                 "active": {
#                     "description": "A boolean indicating activity.",
#                     "type": "boolean"}}}))

#         error = self.assertRaises(ServiceConfigValueError,
#                                   self.config.validate, {"active": "Blob"})
#         self.assertEquals(str(error), "Invalid value for active: Blob")

#         data = self.config.validate({"active": "False"})
#         self.assertEqual(data, {"active": False})
#         data = self.config.validate({"active": "True"})
#         self.assertEqual(data, {"active": True})
#         data = self.config.validate({"active": True})
#         self.assertEqual(data, {"active": True})

#     def test_validate_integer(self):
#         self.config.parse(sample_configuration)

#         error = self.assertRaises(ServiceConfigValueError,
#                                   self.config.validate, {"skill-level": "NaN"})
#         self.assertEquals(str(error), "Invalid value for skill-level: NaN")

#         data = self.config.validate({"skill-level": "9001"})
#         # its over 9000!
#         self.assertEqual(data, {"skill-level": 9001})

#     def test_validate_with_obsolete_str(self):
#         """
#         Test the handling for the obsolete 'str' option type (it's
#         'string' now). Remove support for it after a while, and take
#         this test with it.
#         """
#         config = serializer.yaml_load(sample_configuration)
#         config["options"]["title"]["type"] = "str"
#         obsolete_config = serializer.yaml_dump(config)

#         sio = StringIO()
#         self.patch(sys, "stderr", sio)

#         self.config.parse(obsolete_config)
#         data = self.config.validate({"title": "Helpful Title"})
#         self.assertEqual(data["title"], "Helpful Title")
#         self.assertIn("obsolete 'str'", sio.getvalue())

#         # Trying it again, it should not warn since we don't want
#         # to pester the charm author.
#         sio.truncate(0)
#         self.config.parse(obsolete_config)
#         data = self.config.validate({"title": "Helpful Title"})
#         self.assertEqual(data["title"], "Helpful Title")
#         self.assertEqual(sio.getvalue(), "")
