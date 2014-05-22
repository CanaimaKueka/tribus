import logging

from zookeeper import NodeExistsException, NoNodeException

from twisted.internet.defer import (
    DeferredList, inlineCallbacks, returnValue, succeed, FirstError)

from tribus.common import under
from juju.state.charm import CharmStateManager
from juju.state.errors import CharmStateNotFound, StateChanged

log = logging.getLogger("tribus.common.charms")


class CharmPublisher(object):
    """
    Publishes a charm to an environment.
    """

    def __init__(self, client, storage):
        self._client = client
        self._storage = storage
        self._charm_state_manager = CharmStateManager(self._client)
        self._charm_add_queue = []
        self._charm_state_cache = {}

    @classmethod
    @inlineCallbacks
    def for_environment(cls, environment):
        provider = environment.get_machine_provider()
        storage = provider.get_file_storage()
        client = yield provider.connect()
        returnValue(cls(client, storage))

    @inlineCallbacks
    def add_charm(self, charm_id, charm):
        """Schedule a charm for addition to an juju environment.

        Returns true if the charm is scheduled for upload, false if
        the charm is already present in juju.
        """
        self._charm_add_queue.append((charm_id, charm))
        if charm_id in self._charm_state_cache:
            returnValue(False)
        try:
            state = yield self._charm_state_manager.get_charm_state(
                charm_id)
        except CharmStateNotFound:
            pass
        else:
            log.info("Using cached charm version of %s" % charm.metadata.name)
            self._charm_state_cache[charm_id] = state
            returnValue(False)
        returnValue(True)

    def _publish_one(self, charm_id, charm):
        if charm_id in self._charm_state_cache:
            return succeed(self._charm_state_cache[charm_id])

        bundle = charm.as_bundle()
        charm_file = open(bundle.path, "rb")
        charm_store_path = under.quote(
            "%s:%s" % (charm_id, bundle.get_sha256()))

        def close_charm_file(passthrough):
            charm_file.close()
            return passthrough

        def get_charm_url(result):
            return self._storage.get_url(charm_store_path)

        d = self._storage.put(charm_store_path, charm_file)
        d.addBoth(close_charm_file)
        d.addCallback(get_charm_url)
        d.addCallback(self._cb_store_charm_state, charm_id, bundle)
        d.addErrback(self._eb_verify_duplicate, charm_id, bundle)
        return d

    def publish(self):
        """Publish all added charms to provider storage and zookeeper.

        Returns the charm_state of all scheduled charms.
        """
        publish_deferreds = []
        for charm_id, charm in self._charm_add_queue:
            publish_deferreds.append(self._publish_one(charm_id, charm))

        publish_deferred = DeferredList(publish_deferreds,
                                        fireOnOneErrback=1,
                                        consumeErrors=1)
        # callbacks and deferreds to unwind the dlist
        publish_deferred.addCallback(self._cb_extract_charm_state)
        publish_deferred.addErrback(self._eb_extract_error)
        return publish_deferred

    def _cb_extract_charm_state(self, result):
        return [r[1] for r in result]

    def _eb_extract_error(self, failure):
        failure.trap(FirstError)
        return failure.value.subFailure

    def _cb_store_charm_state(self, charm_url, charm_id, charm):
        return self._charm_state_manager.add_charm_state(
            charm_id, charm, charm_url)

    @inlineCallbacks
    def _eb_verify_duplicate(self, failure, charm_id, charm):
        """Detects duplicates vs. conflicts, raises stateerror on conflict."""
        failure.trap(NodeExistsException)

        try:
            charm_state = \
                yield self._charm_state_manager.get_charm_state(charm_id)
        except NoNodeException:
            # Check if the state goes away due to concurrent removal
            msg = "Charm removed concurrently during publish, please retry."
            raise StateChanged(msg)

        if charm_state.get_sha256() != charm.get_sha256():
            msg = "Concurrent upload of charm has different checksum %s" % (
                charm_id)
            raise StateChanged(msg)
