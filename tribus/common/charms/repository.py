import json
import logging
import os
import tempfile
import urllib
import urlparse
import yaml

from tribus.common.charms.provider import get_charm_from_path
from tribus.common.charms.url import CharmURL, CharmCollection
from tribus.common.errors import FileNotFound
from tribus.common.utils import list_dirs
from tribus.common import under

from tribus.common.charms.errors import (
    CharmNotFound, CharmError, RepositoryNotFound, ServiceConfigValueError)

log = logging.getLogger("tribus.common.charms")

CS_STORE_URL = "https://store.juju.ubuntu.com"


def _makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def _cache_key(charm_url):
    charm_url.assert_revision()
    return under.quote("%s.charm" % charm_url)


class LocalCharmRepository(object):
    """Charm repository in a local directory."""

    type = "local"

    def __init__(self, path):
        if path is None or not os.path.isdir(path):
            raise RepositoryNotFound(path)
        self.path = path


    def list(self):
        schema = "local"
        col = CharmCollection(schema)
        charms = []
        
        for l in list_dirs(self.path):
            charmurl = CharmURL(col, l, None)
            charm =  self.find(charmurl)
            if charm:
                charms.append(charm)
        
        return charms
                
    def _collection(self, collection):
        path = os.path.join(self.path, collection.series)
        if not os.path.exists(path):
            return

        for dentry in os.listdir(path):
            if dentry.startswith("."):
                continue
            dentry_path = os.path.join(path, dentry)
            try:
                yield get_charm_from_path(dentry_path)
            except FileNotFound:
                continue
            # There is a broken charm in the repo, but that
            # shouldn't stop us from continuing
            except yaml.YAMLError, e:
                # Log yaml errors for feedback to developers.
                log.warning("Charm %r has a YAML error: %s", dentry, e)
                continue
            except (CharmError, ServiceConfigValueError), e:
                # Log invalid config.yaml and metadata.yaml semantic errors
                log.warning("Charm %r has an error: %r %s", dentry, e, e)
                continue
            except CharmNotFound:
                # This could just be a random directory/file in the repo
                continue
            except Exception, e:
                # Catch all (perms, unknowns, etc)
                log.warning(
                    "Unexpected error while processing %s: %r",
                    dentry, e)

    def find(self, charm_url):
        """Find a charm with the given name.

        If multiple charms are found with different versions, the most
        recent one (greatest revision) will be returned.
        """
        assert charm_url.collection.schema == "local", "schema mismatch"
        latest = None
        for charm in self._collection(charm_url.collection):
            if charm.metadata.name == charm_url.name:
                if charm.get_revision() == charm_url.revision:
                    return charm
                if (latest is None or
                    latest.get_revision() < charm.get_revision()):
                    latest = charm

        if latest is None or charm_url.revision is not None:
            return CharmNotFound(self.path, charm_url)

        return latest

    def latest(self, charm_url):
        d = self.find(charm_url.with_revision(None))
        d.addCallback(lambda c: c.get_revision())
        return d

    def __str__(self):
        return "local charm repository: %s" % self.path


def resolve(vague_name, repository_path, default_series):
    """Get a Charm and associated identifying information

    :param str vague_name: a lazily specified charm name, suitable for use with
        :meth:`CharmURL.infer`

    :param repository_path: where on the local filesystem to find a repository
        (only currently meaningful when `charm_name` is specified with
        `"local:"`)
    :type repository_path: str or None

    :param str default_series: the Ubuntu series to insert when `charm_name` is
        inadequately specified.

    :return: a tuple of a :class:`tribus.common.charms.url.CharmURL` and a
        :class:`tribus.common.charms.base.CharmBase` subclass, which together contain
        both the charm's data and all information necessary to specify its
        source.
    """
    url = CharmURL.infer(vague_name, default_series)
    repo = LocalCharmRepository(repository_path)

    return repo, url
