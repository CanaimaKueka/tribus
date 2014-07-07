# from juju.charm.errors import CharmURLError
# from juju.charm.url import CharmCollection, CharmURL
# from juju.lib.testing import TestCase


# class CharmCollectionTest(TestCase):

#     def test_str(self):
#         self.assertEquals(
#             str(CharmCollection("foo", "bar", "baz")), "foo:~bar/baz")
#         self.assertEquals(
#             str(CharmCollection("ping", None, "pong")), "ping:pong")


# class CharmURLTest(TestCase):

#     def assert_url(self, url, schema, user, series, name, rev):
#         self.assertEquals(url.collection.schema, schema)
#         self.assertEquals(url.collection.user, user)
#         self.assertEquals(url.collection.series, series)
#         self.assertEquals(url.name, name)
#         self.assertEquals(url.revision, rev)

#     def assert_error(self, err, url_str, message):
#         self.assertEquals(
#             str(err), "Bad charm URL %r: %s" % (url_str, message))

#     def assert_parse(self, string, schema, user, series, name, rev):
#         url = CharmURL.parse(string)
#         self.assert_url(url, schema, user, series, name, rev)
#         self.assertEquals(str(url), string)
#         self.assertEquals(url.path, string.split(":", 1)[1])

#     def test_parse(self):
#         self.assert_parse(
#             "cs:~user/series/name", "cs", "user", "series", "name", None)
#         self.assert_parse(
#             "cs:~user/series/name-0", "cs", "user", "series", "name", 0)
#         self.assert_parse(
#             "cs:series/name", "cs", None, "series", "name", None)
#         self.assert_parse(
#             "cs:series/name-0", "cs", None, "series", "name", 0)
#         self.assert_parse(
#             "cs:series/name0", "cs", None, "series", "name0", None)
#         self.assert_parse(
#             "cs:series/n0-0n-n0", "cs", None, "series", "n0-0n-n0", None)
#         self.assert_parse(
#             "local:series/name", "local", None, "series", "name", None)
#         self.assert_parse(
#             "local:series/name-0", "local", None, "series", "name", 0)

#     def assert_cannot_parse(self, string, message):
#         err = self.assertRaises(CharmURLError, CharmURL.parse, string)
#         self.assert_error(err, string, message)

#     def test_cannot_parse(self):
#         self.assert_cannot_parse(
#             None, "not a string type")
#         self.assert_cannot_parse(
#             "series/name-1", "no schema specified")
#         self.assert_cannot_parse(
#             "bs:~user/series/name-1", "invalid schema")
#         self.assert_cannot_parse(
#             "cs:~1/series/name-1", "invalid user")
#         self.assert_cannot_parse(
#             "cs:~user/1/name-1", "invalid series")
#         self.assert_cannot_parse(
#             "cs:~user/series/name-1-2", "invalid name")
#         self.assert_cannot_parse(
#             "cs:~user/series/name-1-n-2", "invalid name")
#         self.assert_cannot_parse(
#             "cs:~user/series/name--a-2", "invalid name")
#         self.assert_cannot_parse(
#             "cs:~user/series/huh/name-1", "invalid form")
#         self.assert_cannot_parse(
#             "cs:~user/name", "no series specified")
#         self.assert_cannot_parse(
#             "cs:name", "invalid form")
#         self.assert_cannot_parse(
#             "local:~user/series/name", "users not allowed in local URLs")
#         self.assert_cannot_parse(
#             "local:~user/name", "users not allowed in local URLs")
#         self.assert_cannot_parse(
#             "local:name", "invalid form")

#     def test_revision(self):
#         url1 = CharmURL.parse("cs:foo/bar")
#         error = self.assertRaises(CharmURLError, url1.assert_revision)
#         self.assertEquals(
#             str(error), "Bad charm URL 'cs:foo/bar': expected a revision")

#         url2 = url1.with_revision(0)
#         url1.collection.schema = "local" # change url1, verify deep copied
#         url2.assert_revision()
#         self.assertEquals(str(url2), "cs:foo/bar-0")

#         url3 = url2.with_revision(999)
#         url3.assert_revision()
#         self.assertEquals(str(url3), "cs:foo/bar-999")

#     def assert_infer(self, string, schema, user, series, name, rev):
#         url = CharmURL.infer(string, "default")
#         self.assert_url(url, schema, user, series, name, rev)

#     def test_infer(self):
#         self.assert_infer(
#             "name", "cs", None, "default", "name", None)
#         self.assert_infer(
#             "name-0", "cs", None, "default", "name", 0)
#         self.assert_infer(
#             "series/name", "cs", None, "series", "name", None)
#         self.assert_infer(
#             "series/name-0", "cs", None, "series", "name", 0)
#         self.assert_infer(
#             "cs:name", "cs", None, "default", "name", None)
#         self.assert_infer(
#             "cs:name-0", "cs", None, "default", "name", 0)
#         self.assert_infer(
#             "cs:~user/name", "cs", "user", "default", "name", None)
#         self.assert_infer(
#             "cs:~user/name-0", "cs", "user", "default", "name", 0)
#         self.assert_infer(
#             "local:name", "local", None, "default", "name", None)
#         self.assert_infer(
#             "local:name-0", "local", None, "default", "name", 0)

#     def test_cannot_infer(self):
#         err = self.assertRaises(
#             CharmURLError, CharmURL.infer, "name", "invalid!series")
#         self.assertEquals(
#             str(err),
#             "Bad charm URL 'cs:invalid!series/name': invalid series (URL "
#             "inferred from 'name')")

#         err = self.assertRaises(
#             CharmURLError, CharmURL.infer, "~user/name", "default")
#         self.assertEquals(
#             str(err),
#             "Bad charm URL '~user/name': a URL with a user must specify a "
#             "schema")
