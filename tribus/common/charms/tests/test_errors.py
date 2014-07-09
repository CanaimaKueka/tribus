# import os

# from juju.charm.errors import (
#     CharmURLError, CharmNotFound, InvalidCharmHook, NewerCharmNotFound,
#     RepositoryNotFound, ServiceConfigError, InvalidCharmFile, MetaDataError)
# from juju.errors import CharmError, JujuError

# from juju.lib.testing import TestCase


# class CharmErrorsTest(TestCase):

#     def test_NewerCharmNotFound(self):
#         error = NewerCharmNotFound("local:name:21")
#         self.assertEquals(
#             str(error),
#             "Charm 'local:name:21' is the latest revision known")
#         self.assertTrue(isinstance(error, CharmError))

#     def test_CharmURLError(self):
#         error = CharmURLError("foobar:/adfsa:slashot", "bad magic")
#         self.assertEquals(
#             str(error),
#             "Bad charm URL 'foobar:/adfsa:slashot': bad magic")
#         self.assertTrue(isinstance(error, CharmError))

#     def test_CharmNotFound(self):
#         error = CharmNotFound("/path", "cassandra")
#         self.assertEquals(
#             str(error),
#             "Charm 'cassandra' not found in repository /path")
#         self.assertTrue(isinstance(error, JujuError))

#     def test_InvalidCharmHook(self):
#         error = InvalidCharmHook("mysql", "magic-relation-changed")
#         self.assertEquals(
#             str(error),
#             "Charm 'mysql' does not contain hook 'magic-relation-changed'")
#         self.assertTrue(isinstance(error, CharmError))

#     def test_InvalidCharmFile(self):
#         error = InvalidCharmFile("mysql", "hooks/foobar", "bad file")
#         self.assertEquals(
#             str(error),
#             "Charm 'mysql' invalid file 'hooks/foobar' bad file")
#         self.assertTrue(isinstance(error, CharmError))

#     def test_MetaDataError(self):
#         error = MetaDataError("foobar is bad")
#         self.assertEquals(
#             str(error),
#             "foobar is bad")
#         self.assertTrue(isinstance(error, CharmError))

#     def test_RepositoryNotFound(self):
#         error = RepositoryNotFound(None)
#         self.assertEquals(str(error), "No repository specified")
#         self.assertTrue(isinstance(error, JujuError))

#         path = os.path.join(self.makeDir(), "missing")
#         error = RepositoryNotFound(path)
#         self.assertEquals(str(error), "No repository found at %r" % path)
#         self.assertTrue(isinstance(error, JujuError))

#     def test_ServiceConfigError(self):
#         error = ServiceConfigError("foobar", "blah")
#         self.assertEquals(str(error), "Error processing 'foobar': blah")
#         self.assertTrue(isinstance(error, JujuError))
