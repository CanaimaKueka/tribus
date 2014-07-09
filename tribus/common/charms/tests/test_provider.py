# import os
# import inspect

# from juju.lib.testing import TestCase
# from juju.charm import tests
# from juju.charm.provider import get_charm_from_path

# sample_directory = os.path.join(
#     os.path.dirname(inspect.getabsfile(tests)), "repository", "series", "dummy")


# class CharmFromPathTest(TestCase):

#     def test_charm_from_path(self):
#         # from a directory
#         charm = get_charm_from_path(sample_directory)
#         assert charm.get_sha256()

#         filename = self.makeFile(suffix=".charm")
#         charm.make_archive(filename)

#         # and from a bundle
#         charm = get_charm_from_path(filename)
#         self.assertEquals(charm.path, filename)
#         self.assertInstance(charm.get_sha256(), basestring)

#         # and validate the implementation detail that calling it twice
#         # doesn't result in an error after caching the callable
#         charm = get_charm_from_path(filename)
#         self.assertEquals(charm.path, filename)
#         self.assertInstance(charm.get_sha256(), basestring)
