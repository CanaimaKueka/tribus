# import json
# import os
# import inspect
# import shutil

# from twisted.internet.defer import fail, inlineCallbacks, succeed
# from twisted.web.error import Error
# from txaws.client.ssl import VerifyingContextFactory


# from juju.charm.directory import CharmDirectory
# from juju.charm.errors import CharmNotFound, CharmURLError, RepositoryNotFound
# from juju.charm.repository import (
#     LocalCharmRepository, RemoteCharmRepository, resolve, CS_STORE_URL)
# from juju.charm.url import CharmURL
# from juju.charm import provider
# from juju.errors import CharmError
# from juju.lib import under

# from juju.charm import tests
# from juju.lib.mocker import ANY, MATCH
# from juju.lib.testing import TestCase


# unbundled_repository = os.path.join(
#     os.path.dirname(inspect.getabsfile(tests)), "repository")


# class RepositoryTestBase(TestCase):

#     @inlineCallbacks
#     def setUp(self):
#         yield super(RepositoryTestBase, self).setUp()
#         self.bundled_repo_path = self.makeDir()
#         os.mkdir(os.path.join(self.bundled_repo_path, "series"))
#         self.unbundled_repo_path = self.makeDir()

#         os.rmdir(self.unbundled_repo_path)

#         shutil.copytree(unbundled_repository, self.unbundled_repo_path)

#         self.sample_dir1 = os.path.join(
#             self.unbundled_repo_path, "series", "old")
#         self.sample_dir2 = os.path.join(
#             self.unbundled_repo_path, "series", "new")


# class LocalRepositoryTest(RepositoryTestBase):

#     def setUp(self):
#         super(LocalRepositoryTest, self).setUp()

#         # bundle sample charms
#         CharmDirectory(self.sample_dir1).make_archive(
#             os.path.join(self.bundled_repo_path, "series", "old.charm"))
#         CharmDirectory(self.sample_dir2).make_archive(
#             os.path.join(self.bundled_repo_path, "series", "new.charm"))

#         # define repository objects
#         self.repository1 = LocalCharmRepository(self.unbundled_repo_path)
#         self.repository2 = LocalCharmRepository(self.bundled_repo_path)
#         self.output = self.capture_logging("juju.charm")

#     def assert_there(self, name, repo, revision, latest_revision=None):
#         url = self.charm_url(name)
#         charm = yield repo.find(url)
#         self.assertEquals(charm.get_revision(), revision)
#         latest = yield repo.latest(url)
#         self.assertEquals(latest, latest_revision or revision)

#     @inlineCallbacks
#     def assert_not_there(self, name, repo, revision=None):
#         url = self.charm_url(name)
#         msg = "Charm 'local:series/%s' not found in repository %s" % (
#             name, repo.path)
#         err = yield self.assertFailure(repo.find(url), CharmNotFound)
#         self.assertEquals(str(err), msg)
#         if revision is None:
#             err = yield self.assertFailure(repo.latest(url), CharmNotFound)
#             self.assertEquals(str(err), msg)

#     def charm_url(self, name):
#         return CharmURL.parse("local:series/" + name)

#     def test_no_path(self):
#         err = self.assertRaises(RepositoryNotFound, LocalCharmRepository, None)
#         self.assertEquals(str(err), "No repository specified")

#     def test_bad_path(self):
#         path = os.path.join(self.makeDir(), "blah")
#         err = self.assertRaises(RepositoryNotFound, LocalCharmRepository, path)
#         self.assertEquals(str(err), "No repository found at %r" % path)
#         with open(path, "w"):
#             pass
#         err = self.assertRaises(RepositoryNotFound, LocalCharmRepository, path)
#         self.assertEquals(str(err), "No repository found at %r" % path)

#     def test_find_inappropriate_url(self):
#         url = CharmURL.parse("cs:foo/bar")
#         err = self.assertRaises(AssertionError, self.repository1.find, url)
#         self.assertEquals(str(err), "schema mismatch")

#     def test_completely_missing(self):
#         return self.assert_not_there("zebra", self.repository1)

#     def test_unknown_files_ignored(self):
#         self.makeFile(
#             "Foobar",
#             path=os.path.join(self.repository1.path, "series", "zebra"))
#         return self.assert_not_there("zebra", self.repository1)

#     @inlineCallbacks
#     def test_random_error_logged(self):
#         get_charm = self.mocker.replace(provider.get_charm_from_path)
#         get_charm(ANY)
#         self.mocker.throw(SyntaxError("magic"))
#         self.mocker.count(0, 3)
#         self.mocker.replay()

#         yield self.assertFailure(
#             self.repository1.find(self.charm_url("zebra")),
#             CharmNotFound)

#         self.assertIn(
#             "Unexpected error while processing",
#             self.output.getvalue())
#         self.assertIn(
#             "SyntaxError('magic',)",
#             self.output.getvalue())

#     def test_unknown_directories_ignored(self):
#         self.makeDir(
#             path=os.path.join(self.repository1.path, "series", "zebra"))
#         return self.assert_not_there("zebra", self.repository1)

#     @inlineCallbacks
#     def test_broken_charm_metadata_ignored(self):
#         charm_path = self.makeDir(
#             path=os.path.join(self.repository1.path, "series", "zebra"))
#         fh = open(os.path.join(charm_path, "metadata.yaml"), "w+")
#         fh.write("""\
#         description: helo
# name: hi
# requires: {interface: zebra
# revision: 0
# summary: hola""")
#         fh.close()
#         yield self.assertFailure(
#             self.repository1.find(self.charm_url("zebra")), CharmNotFound)
#         output = self.output.getvalue()
#         self.assertIn(
#             "Charm 'zebra' has a YAML error", output)
#         self.assertIn(
#             "%s/series/zebra/metadata.yaml" % self.repository1.path, output)

#     @inlineCallbacks
#     def test_broken_charm_config_ignored(self):
#         """YAML Errors propogate to the log, but the search continues."""
#         fh = open(
#             os.path.join(
#                 self.repository1.path, "series", "mysql", "config.yaml"),
#             "w+")

#         fh.write("""\
#         description: helo
# name: hi
# requires: {interface: zebra
# revision: 0
# summary: hola""")
#         fh.close()
#         yield self.repository1.find(self.charm_url("sample"))
#         output = self.output.getvalue()
#         self.assertIn(
#             "Charm 'mysql' has a YAML error", output)
#         self.assertIn(
#             "%s/series/mysql/config.yaml" % self.repository1.path, output)

#     @inlineCallbacks
#     def test_ignore_dot_files(self):
#         """Dot files are ignored when browsing the repository."""
#         fh = open(
#             os.path.join(
#                 self.repository1.path, "series", ".foo"),
#             "w+")

#         fh.write("Something")
#         fh.close()
#         yield self.repository1.find(self.charm_url("sample"))
#         output = self.output.getvalue()
#         self.assertNotIn("Charm '.foo' has an error", output)

#     @inlineCallbacks
#     def test_invalid_charm_config_ignored(self):
#         fh = open(
#             os.path.join(
#                 self.repository1.path, "series", "mysql", "config.yaml"),
#             "w+")

#         fh.write("foobar: {}")
#         fh.close()
#         stream = self.capture_logging("juju.charm")
#         yield self.assertFailure(
#             self.repository1.find(self.charm_url("mysql")), CharmNotFound)
#         output = stream.getvalue()
#         self.assertIn(
#             "Charm 'mysql' has an error", output)
#         self.assertIn(
#             "%s/series/mysql/config.yaml" % self.repository1.path, output)

#     def test_repo_type(self):
#         self.assertEqual(self.repository1.type, "local")

#     @inlineCallbacks
#     def test_success_unbundled(self):
#         yield self.assert_there("sample", self.repository1, 2)
#         yield self.assert_there("sample-1", self.repository1, 1, 2)
#         yield self.assert_there("sample-2", self.repository1, 2)
#         yield self.assert_not_there("sample-3", self.repository1, 2)

#     @inlineCallbacks
#     def test_success_bundled(self):
#         yield self.assert_there("sample", self.repository2, 2)
#         yield self.assert_there("sample-1", self.repository2, 1, 2)
#         yield self.assert_there("sample-2", self.repository2, 2)
#         yield self.assert_not_there("sample-3", self.repository2, 2)

#     @inlineCallbacks
#     def test_no_revision_gets_latest(self):
#         yield self.assert_there("sample", self.repository1, 2)
#         yield self.assert_there("sample-1", self.repository1, 1, 2)
#         yield self.assert_there("sample-2", self.repository1, 2)
#         yield self.assert_not_there("sample-3", self.repository1, 2)

#         revision_path = os.path.join(
#             self.repository1.path, "series/old/revision")
#         with open(revision_path, "w") as f:
#             f.write("3")

#         yield self.assert_there("sample", self.repository1, 3)
#         yield self.assert_not_there("sample-1", self.repository1, 3)
#         yield self.assert_there("sample-2", self.repository1, 2, 3)
#         yield self.assert_there("sample-3", self.repository1, 3)


# class RemoteRepositoryTest(RepositoryTestBase):

#     def setUp(self):
#         super(RemoteRepositoryTest, self).setUp()
#         self.cache_path = os.path.join(
#             self.makeDir(), "notexistyet")
#         self.download_path = os.path.join(self.cache_path, "downloads")

#         def delete():
#             if os.path.exists(self.cache_path):
#                 shutil.rmtree(self.cache_path)
#         self.addCleanup(delete)

#         self.charm = CharmDirectory(
#             os.path.join(self.unbundled_repo_path, "series", "dummy"))
#         with open(self.charm.as_bundle().path, "rb") as f:
#             self.bundle_data = f.read()
#         self.sha256 = self.charm.as_bundle().get_sha256()
#         self.getPage = self.mocker.replace("twisted.web.client.getPage")
#         self.downloadPage = self.mocker.replace(
#             "twisted.web.client.downloadPage")

#     def repo(self, url_base):
#         return RemoteCharmRepository(url_base, self.cache_path)

#     def cache_location(self, url_str, revision):
#         charm_url = CharmURL.parse(url_str)
#         cache_key = under.quote(
#             "%s.charm" % (charm_url.with_revision(revision)))
#         return os.path.join(self.cache_path, cache_key)

#     def charm_info(self, url_str, revision, warnings=None, errors=None):
#         info = {"revision": revision, "sha256": self.sha256}
#         if errors:
#             info["errors"] = errors
#         if warnings:
#             info["warnings"] = warnings
#         return json.dumps({url_str: info})

#     def mock_charm_info(self, url, result):
#         def match_context(value):
#             return isinstance(value, VerifyingContextFactory)
#         self.getPage(url, contextFactory=MATCH(match_context))
#         self.mocker.result(result)

#     def mock_download(self, url, error=None):
#         def match_context(value):
#             return isinstance(value, VerifyingContextFactory)
#         self.downloadPage(url, ANY, contextFactory=MATCH(match_context))
#         if error:
#             return self.mocker.result(fail(error))

#         def download(_, path, contextFactory):
#             self.assertTrue(path.startswith(self.download_path))
#             with open(path, "wb") as f:
#                 f.write(self.bundle_data)
#             return succeed(None)
#         self.mocker.call(download)

#     @inlineCallbacks
#     def assert_find_uncached(self, dns_name, url_str, info_url, find_url):
#         self.mock_charm_info(info_url, succeed(self.charm_info(url_str, 1)))
#         self.mock_download(find_url)
#         self.mocker.replay()

#         repo = self.repo(dns_name)
#         charm = yield repo.find(CharmURL.parse(url_str))
#         self.assertEquals(charm.get_sha256(), self.sha256)
#         self.assertEquals(charm.path, self.cache_location(url_str, 1))
#         self.assertEquals(os.listdir(self.download_path), [])

#     @inlineCallbacks
#     def assert_find_cached(self, dns_name, url_str, info_url):
#         os.makedirs(self.cache_path)
#         cache_location = self.cache_location(url_str, 1)
#         shutil.copy(self.charm.as_bundle().path, cache_location)

#         self.mock_charm_info(info_url, succeed(self.charm_info(url_str, 1)))
#         self.mocker.replay()

#         repo = self.repo(dns_name)
#         charm = yield repo.find(CharmURL.parse(url_str))
#         self.assertEquals(charm.get_sha256(), self.sha256)
#         self.assertEquals(charm.path, cache_location)

#     def assert_find_error(self, dns_name, url_str, err_type, message):
#         self.mocker.replay()
#         repo = self.repo(dns_name)
#         d = self.assertFailure(repo.find(CharmURL.parse(url_str)), err_type)

#         def verify(error):
#             self.assertEquals(str(error), message)
#         d.addCallback(verify)
#         return d

#     @inlineCallbacks
#     def assert_latest(self, dns_name, url_str, revision):
#         self.mocker.replay()
#         repo = self.repo(dns_name)
#         result = yield repo.latest(CharmURL.parse(url_str))
#         self.assertEquals(result, revision)

#     def assert_latest_error(self, dns_name, url_str, err_type, message):
#         self.mocker.replay()
#         repo = self.repo(dns_name)
#         d = self.assertFailure(repo.latest(CharmURL.parse(url_str)), err_type)

#         def verify(error):
#             self.assertEquals(str(error), message)
#         d.addCallback(verify)
#         return d

#     def test_find_plain_uncached_no_stat(self):
#         self.change_environment(JUJU_TESTING="1")
#         return self.assert_find_uncached(
#             "https://somewhe.re", "cs:series/name",
#             "https://somewhe.re/charm-info?charms=cs%3Aseries/name&stats=0",
#             "https://somewhe.re/charm/series/name-1?stats=0")

#     def test_find_plain_uncached(self):
#         return self.assert_find_uncached(
#             "https://somewhe.re", "cs:series/name",
#             "https://somewhe.re/charm-info?charms=cs%3Aseries/name",
#             "https://somewhe.re/charm/series/name-1")

#     def test_find_revision_uncached(self):
#         return self.assert_find_uncached(
#             "https://somewhe.re", "cs:series/name-1",
#             "https://somewhe.re/charm-info?charms=cs%3Aseries/name-1",
#             "https://somewhe.re/charm/series/name-1")

#     def test_find_user_uncached(self):
#         return self.assert_find_uncached(
#             "https://somewhereel.se", "cs:~user/srs/name",
#             "https://somewhereel.se/charm-info?charms=cs%3A%7Euser/srs/name",
#             "https://somewhereel.se/charm/%7Euser/srs/name-1")

#     def test_find_plain_cached(self):
#         return self.assert_find_cached(
#             "https://somewhe.re", "cs:series/name",
#             "https://somewhe.re/charm-info?charms=cs%3Aseries/name")

#     def test_find_revision_cached(self):
#         return self.assert_find_cached(
#             "https://somewhe.re", "cs:series/name-1",
#             "https://somewhe.re/charm-info?charms=cs%3Aseries/name-1")

#     def test_find_user_cached(self):
#         return self.assert_find_cached(
#             "https://somewhereel.se", "cs:~user/srs/name",
#             "https://somewhereel.se/charm-info?charms=cs%3A%7Euser/srs/name")

#     def test_find_info_http_error(self):
#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name",
#             fail(Error("500")))
#         return self.assert_find_error(
#             "https://anoth.er", "cs:series/name", CharmNotFound,
#             "Charm 'cs:series/name' not found in repository https://anoth.er")

#     @inlineCallbacks
#     def test_find_info_store_warning(self):
#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name-1",
#             succeed(self.charm_info(
#                 "cs:series/name-1", 1, warnings=["omg", "halp"])))
#         self.mock_download("https://anoth.er/charm/series/name-1")
#         self.mocker.replay()

#         repo = self.repo("https://anoth.er")
#         log = self.capture_logging("juju.charm")
#         charm = yield repo.find(CharmURL.parse("cs:series/name-1"))
#         self.assertIn("omg", log.getvalue())
#         self.assertIn("halp", log.getvalue())
#         self.assertEquals(charm.get_sha256(), self.sha256)

#     def test_find_info_store_error(self):
#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name-101",
#             succeed(self.charm_info(
#                 "cs:series/name-101", 101, errors=["oh", "noes"])))
#         return self.assert_find_error(
#             "https://anoth.er", "cs:series/name-101", CharmError,
#             "Error processing 'cs:series/name-101': oh; noes")

#     def test_find_info_bad_revision(self):
#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name-99",
#             succeed(self.charm_info("cs:series/name-99", 1)))
#         return self.assert_find_error(
#             "https://anoth.er", "cs:series/name-99", AssertionError,
#             "bad url revision")

#     def test_find_download_error(self):
#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name",
#             succeed(json.dumps({"cs:series/name": {"revision": 123}})))
#         self.mock_download(
#             "https://anoth.er/charm/series/name-123", Error("999"))
#         return self.assert_find_error(
#             "https://anoth.er", "cs:series/name", CharmNotFound,
#             "Charm 'cs:series/name-123' not found in repository "
#             "https://anoth.er")

#     def test_find_charm_revision_mismatch(self):
#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name",
#             succeed(json.dumps({"cs:series/name": {"revision": 99}})))
#         self.mock_download("https://anoth.er/charm/series/name-99")
#         return self.assert_find_error(
#             "https://anoth.er", "cs:series/name", AssertionError,
#             "bad charm revision")

#     @inlineCallbacks
#     def test_find_downloaded_hash_mismatch(self):
#         cache_location = self.cache_location("cs:series/name-1", 1)
#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name",
#             succeed(json.dumps(
#                 {"cs:series/name": {"revision": 1, "sha256": "NO YUO"}})))
#         self.mock_download("https://anoth.er/charm/series/name-1")
#         yield self.assert_find_error(
#             "https://anoth.er", "cs:series/name", CharmError,
#             "Error processing 'cs:series/name-1 (downloaded)': SHA256 "
#             "mismatch")
#         self.assertFalse(os.path.exists(cache_location))

#     @inlineCallbacks
#     def test_find_cached_hash_mismatch(self):
#         os.makedirs(self.cache_path)
#         cache_location = self.cache_location("cs:series/name-1", 1)
#         shutil.copy(self.charm.as_bundle().path, cache_location)

#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name",
#             succeed(json.dumps(
#                 {"cs:series/name": {"revision": 1, "sha256": "NO YUO"}})))
#         yield self.assert_find_error(
#             "https://anoth.er", "cs:series/name", CharmError,
#             "Error processing 'cs:series/name-1 (cached)': SHA256 mismatch")
#         self.assertFalse(os.path.exists(cache_location))

#     def test_latest_plain(self):
#         self.mock_charm_info(
#             "https://somewhe.re/charm-info?charms=cs%3Afoo/bar",
#             succeed(self.charm_info("cs:foo/bar", 99)))
#         return self.assert_latest("https://somewhe.re", "cs:foo/bar-1", 99)

#     def test_latest_user(self):
#         self.mock_charm_info(
#             "https://somewhereel.se/charm-info?charms=cs%3A%7Efee/foo/bar",
#             succeed(self.charm_info("cs:~fee/foo/bar", 123)))
#         return self.assert_latest(
#             "https://somewhereel.se", "cs:~fee/foo/bar", 123)

#     def test_latest_revision(self):
#         self.mock_charm_info(
#             "https://somewhereel.se/charm-info?charms=cs%3A%7Efee/foo/bar",
#             succeed(self.charm_info("cs:~fee/foo/bar", 123)))
#         return self.assert_latest(
#             "https://somewhereel.se", "cs:~fee/foo/bar-99", 123)

#     def test_latest_http_error(self):
#         self.mock_charm_info(
#             "https://andanoth.er/charm-info?charms=cs%3A%7Eblib/blab/blob",
#             fail(Error("404")))
#         return self.assert_latest_error(
#             "https://andanoth.er", "cs:~blib/blab/blob", CharmNotFound,
#             "Charm 'cs:~blib/blab/blob' not found in repository "
#             "https://andanoth.er")

#     @inlineCallbacks
#     def test_latest_store_warning(self):
#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name",
#             succeed(self.charm_info(
#                 "cs:series/name", 1, warnings=["eww", "yuck"])))
#         self.mocker.replay()

#         repo = self.repo("https://anoth.er")
#         log = self.capture_logging("juju.charm")
#         revision = yield repo.latest(CharmURL.parse("cs:series/name-1"))
#         self.assertIn("eww", log.getvalue())
#         self.assertIn("yuck", log.getvalue())
#         self.assertEquals(revision, 1)

#     def test_latest_store_error(self):
#         self.mock_charm_info(
#             "https://anoth.er/charm-info?charms=cs%3Aseries/name",
#             succeed(self.charm_info(
#                 "cs:series/name", 1, errors=["blam", "dink"])))
#         return self.assert_latest_error(
#             "https://anoth.er", "cs:series/name-1", CharmError,
#             "Error processing 'cs:series/name': blam; dink")

#     def test_repo_type(self):
#         self.mocker.replay()
#         self.assertEqual(self.repo("http://fbaro.com").type, "store")


# class ResolveTest(RepositoryTestBase):

#     def assert_resolve_local(self, vague, default, expect):
#         path = self.makeDir()
#         repo, url = resolve(vague, path, default)
#         self.assertEquals(str(url), expect)
#         self.assertTrue(isinstance(repo, LocalCharmRepository))
#         self.assertEquals(repo.path, path)

#     def test_resolve_local(self):
#         self.assert_resolve_local(
#             "local:series/sample", "default", "local:series/sample")
#         self.assert_resolve_local(
#             "local:sample", "default", "local:default/sample")

#     def assert_resolve_remote(self, vague, default, expect):
#         repo, url = resolve(vague, None, default)
#         self.assertEquals(str(url), expect)
#         self.assertTrue(isinstance(repo, RemoteCharmRepository))
#         self.assertEquals(repo.url_base, CS_STORE_URL)

#     def test_resolve_remote(self):
#         self.assert_resolve_remote(
#             "sample", "default", "cs:default/sample")
#         self.assert_resolve_remote(
#             "series/sample", "default", "cs:series/sample")
#         self.assert_resolve_remote(
#             "cs:sample", "default", "cs:default/sample")
#         self.assert_resolve_remote(
#             "cs:series/sample", "default", "cs:series/sample")
#         self.assert_resolve_remote(
#             "cs:~user/sample", "default", "cs:~user/default/sample")
#         self.assert_resolve_remote(
#             "cs:~user/series/sample", "default", "cs:~user/series/sample")

#     def test_resolve_nonsense(self):
#         error = self.assertRaises(
#             CharmURLError, resolve, "blah:whatever", None, "series")
#         self.assertEquals(
#             str(error),
#             "Bad charm URL 'blah:series/whatever': invalid schema (URL "
#             "inferred from 'blah:whatever')")
