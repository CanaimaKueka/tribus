# from juju.charm.base import CharmBase, get_revision
# from juju.charm.metadata import MetaData
# from juju.errors import CharmError
# from juju.lib import serializer
# from juju.lib.testing import TestCase


# class MyCharm(CharmBase):
#     pass


# class CharmBaseTest(TestCase):

#     def setUp(self):
#         self.charm = MyCharm()

#     def assertUnsupported(self, callable, attr_name):
#         try:
#             callable()
#         except NotImplementedError, e:
#             self.assertEquals(str(e),
#                               "MyCharm.%s not supported" % attr_name)
#         else:
#             self.fail("MyCharm.%s didn't fail" % attr_name)

#     def test_unsupported(self):
#         self.assertUnsupported(self.charm.as_bundle, "as_bundle()")
#         self.assertUnsupported(self.charm.get_sha256, "compute_sha256()")
#         self.assertUnsupported(self.charm.compute_sha256, "compute_sha256()")
#         self.assertUnsupported(self.charm.get_revision, "get_revision()")
#         self.assertUnsupported(
#             lambda: self.charm.set_revision(1), "set_revision()")

#     def test_compute_and_cache_sha256(self):
#         """
#         The value computed by compute_sha256() on a child class
#         is returned by get_sha256, and cached permanently.
#         """
#         sha256 = ["mysha"]

#         class CustomCharm(CharmBase):

#             def compute_sha256(self):
#                 return sha256[0]

#         charm = CustomCharm()
#         self.assertEquals(charm.get_sha256(), "mysha")
#         sha256 = ["anothervalue"]
#         # Should still be the same, since the old one was cached.
#         self.assertEquals(charm.get_sha256(), "mysha")


# class GetRevisionTest(TestCase):

#     def assert_good_content(self, content, value):
#         self.assertEquals(get_revision(content, None, None), value)

#     def assert_bad_content(self, content):
#         err = self.assertRaises(
#             CharmError, get_revision, content, None, "path")
#         self.assertEquals(
#             str(err),
#             "Error processing 'path': invalid charm revision %r" % content)

#     def test_with_content(self):
#         self.assert_good_content("0\n", 0)
#         self.assert_good_content("123\n", 123)
#         self.assert_bad_content("")
#         self.assert_bad_content("-1\n")
#         self.assert_bad_content("three hundred and six or so")

#     def test_metadata_fallback(self):
#         metadata = MetaData()
#         self.assertEquals(get_revision(None, metadata, None), None)
#         metadata.parse(
#             serializer.yaml_dump(
#                 {"name": "x", "summary": "y", "description": "z","revision": 33},
#                 ))

#         self.assertEquals(get_revision(None, metadata, None), 33)
