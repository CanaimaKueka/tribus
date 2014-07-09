# import fcntl
# import os
# import zookeeper

# from twisted.internet.defer import inlineCallbacks, fail
# from twisted.python.failure import Failure

# from txzookeeper.tests.utils import deleteTree

# from juju.charm.bundle import CharmBundle
# from juju.charm.directory import CharmDirectory
# from juju.charm.publisher import CharmPublisher
# from juju.charm.tests import local_charm_id
# from juju.lib import under, serializer
# from juju.providers.dummy import FileStorage
# from juju.state.charm import CharmStateManager
# from juju.state.errors import StateChanged

# from juju.environment.tests.test_config import (
#     EnvironmentsConfigTestBase, SAMPLE_ENV)
# from juju.lib.mocker import MATCH

# from .test_repository import RepositoryTestBase


# def _count_open_files():
#     count = 0
#     for sfd in os.listdir("/proc/self/fd"):
#         ifd = int(sfd)
#         if ifd < 3:
#             continue
#         try:
#             fcntl.fcntl(ifd, fcntl.F_GETFD)
#             count += 1
#         except IOError:
#             pass
#     return count


# class CharmPublisherTest(RepositoryTestBase):

#     @inlineCallbacks
#     def setUp(self):
#         super(CharmPublisherTest, self).setUp()
#         zookeeper.set_debug_level(0)

#         self.charm = CharmDirectory(self.sample_dir1)
#         self.charm_id = local_charm_id(self.charm)
#         self.charm_key = under.quote(self.charm_id)
#         # provider storage key
#         self.charm_storage_key = under.quote(
#             "%s:%s" % (self.charm_id, self.charm.get_sha256()))

#         self.client = self.get_zookeeper_client()
#         self.storage_dir = self.makeDir()
#         self.storage = FileStorage(self.storage_dir)
#         self.publisher = CharmPublisher(self.client, self.storage)

#         yield self.client.connect()
#         yield self.client.create("/charms")

#     def tearDown(self):
#         deleteTree("/", self.client.handle)
#         self.client.close()
#         super(CharmPublisherTest, self).tearDown()

#     @inlineCallbacks
#     def test_add_charm_and_publish(self):
#         open_file_count = _count_open_files()
#         yield self.publisher.add_charm(self.charm_id, self.charm)
#         result = yield self.publisher.publish()
#         self.assertEquals(_count_open_files(), open_file_count)

#         children = yield self.client.get_children("/charms")
#         self.assertEqual(children, [self.charm_key])
#         fh = yield self.storage.get(self.charm_storage_key)
#         bundle = CharmBundle(fh)
#         self.assertEqual(self.charm.get_sha256(), bundle.get_sha256())

#         self.assertEqual(
#             result[0].bundle_url, "file://%s/%s" % (
#                 self.storage_dir, self.charm_storage_key))

#     @inlineCallbacks
#     def test_published_charm_sans_unicode(self):
#         yield self.publisher.add_charm(self.charm_id, self.charm)
#         yield self.publisher.publish()
#         data, stat = yield self.client.get("/charms/%s" % self.charm_key)
#         self.assertNotIn("unicode", data)

#     @inlineCallbacks
#     def test_add_charm_with_concurrent(self):
#         """
#         Publishing a charm, that has become published concurrent, after the
#         add_charm, works fine. it will write to storage regardless. The use
#         of a sha256 as part of the storage key is utilized to help ensure
#         uniqueness of bits. The sha256 is also stored with the charm state.

#         This relation betewen the charm state and the binary bits, helps
#         guarantee the property that any published charm in zookeeper will use
#         the binary bits that it was published with.
#         """

#         yield self.publisher.add_charm(self.charm_id, self.charm)

#         concurrent_publisher = CharmPublisher(
#             self.client, self.storage)

#         charm = CharmDirectory(self.sample_dir1)
#         yield concurrent_publisher.add_charm(self.charm_id, charm)

#         yield self.publisher.publish()

#         # modify the charm to create a conflict scenario
#         self.makeFile("zebra",
#                       path=os.path.join(self.sample_dir1, "junk.txt"))

#         # assert the charm now has a different sha post modification
#         modified_charm_sha = charm.get_sha256()
#         self.assertNotEqual(
#             modified_charm_sha,
#             self.charm.get_sha256())

#         # verify publishing raises a stateerror
#         def verify_failure(result):
#             if not isinstance(result, Failure):
#                 self.fail("Should have raised state error")
#             result.trap(StateChanged)
#             return True

#         yield concurrent_publisher.publish().addBoth(verify_failure)

#         # verify the zk state
#         charm_nodes = yield self.client.get_children("/charms")
#         self.assertEqual(charm_nodes, [self.charm_key])

#         content, stat = yield self.client.get(
#             "/charms/%s" % charm_nodes[0])

#         # assert the checksum matches the initially published checksum
#         self.assertEqual(
#             serializer.yaml_load(content)["sha256"],
#             self.charm.get_sha256())

#         store_path = os.path.join(self.storage_dir, self.charm_storage_key)
#         self.assertTrue(os.path.exists(store_path))

#         # and the binary bits where stored
#         modified_charm_storage_key = under.quote(
#             "%s:%s" % (self.charm_id, modified_charm_sha))
#         modified_store_path = os.path.join(
#             self.storage_dir, modified_charm_storage_key)
#         self.assertTrue(os.path.exists(modified_store_path))

#     @inlineCallbacks
#     def test_add_charm_with_concurrent_removal(self):
#         """
#         If a charm is published, and it detects that the charm exists
#         already exists, it will attempt to retrieve the charm state to
#         verify there is no checksum mismatch. If concurrently the charm
#         is removed, the publisher should fail with a statechange error.
#         """
#         manager = self.mocker.patch(CharmStateManager)

#         manager.get_charm_state(self.charm_id)
#         self.mocker.passthrough()

#         def match_charm_bundle(bundle):
#             return isinstance(bundle, CharmBundle)

#         def match_charm_url(url):
#             return url.startswith("file://")

#         manager.add_charm_state(
#             self.charm_id, MATCH(match_charm_bundle), MATCH(match_charm_url))
#         self.mocker.result(fail(zookeeper.NodeExistsException()))

#         manager.get_charm_state(self.charm_id)
#         self.mocker.result(fail(zookeeper.NoNodeException()))
#         self.mocker.replay()

#         yield self.publisher.add_charm(self.charm_id, self.charm)
#         yield self.failUnlessFailure(self.publisher.publish(), StateChanged)

#     @inlineCallbacks
#     def test_add_charm_already_known(self):
#         """Adding an existing charm, is an effective noop, as its not added
#         to the internal publisher queue.
#         """
#         output = self.capture_logging("juju.charm")
#         # Do an initial publishing of the charm
#         scheduled = yield self.publisher.add_charm(self.charm_id, self.charm)
#         self.assertTrue(scheduled)
#         result = yield self.publisher.publish()
#         self.assertEqual(result[0].name, self.charm.metadata.name)

#         publisher = CharmPublisher(self.client, self.storage)
#         scheduled = yield publisher.add_charm(self.charm_id, self.charm)
#         self.assertFalse(scheduled)
#         scheduled = yield publisher.add_charm(self.charm_id, self.charm)
#         self.assertFalse(scheduled)

#         result = yield publisher.publish()
#         self.assertEqual(result[0].name, self.charm.metadata.name)
#         self.assertEqual(result[1].name, self.charm.metadata.name)
#         self.assertIn(
#             "Using cached charm version of %s" % self.charm.metadata.name,
#             output.getvalue())


# class EnvironmentPublisherTest(EnvironmentsConfigTestBase):

#     def setUp(self):
#         super(EnvironmentPublisherTest, self).setUp()
#         self.write_config(SAMPLE_ENV)
#         self.config.load()
#         self.environment = self.config.get("myfirstenv")
#         zookeeper.set_debug_level(0)

#     @inlineCallbacks
#     def test_publisher_for_environment(self):
#         publisher = yield CharmPublisher.for_environment(self.environment)
#         self.assertTrue(isinstance(publisher, CharmPublisher))
