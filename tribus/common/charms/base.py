from tribus.common.errors import CharmError


def get_revision(file_content, metadata, path):
    if file_content is None:
        return metadata.obsolete_revision
    try:
        result = int(file_content.strip())
        if result >= 0:
            return result
    except (ValueError, TypeError):
        pass
    raise CharmError(path, "invalid charm revision %r" % file_content)


class CharmBase(object):
    """Abstract base class for charm implementations.
    """

    _sha256 = None

    def _unsupported(self, attr):
        raise NotImplementedError("%s.%s not supported" %
                                  (self.__class__.__name__, attr))

    def get_revision(self):
        """Get the revision, preferably from the revision file.

        Will fall back to metadata if not available.
        """
        self._unsupported("get_revision()")

    def set_revision(self, revision):
        """Update the revision file, if possible.

        Some subclasses may not be able to do this.
        """
        self._unsupported("set_revision()")

    def as_bundle(self):
        """Transform this charm into a charm bundle, if possible.

        Some subclasses may not be able to do this.
        """
        self._unsupported("as_bundle()")

    def compute_sha256(self):
        """Compute the sha256 for this charm.

        Every charm subclass must implement this.
        """
        self._unsupported("compute_sha256()")

    def get_sha256(self):
        """Return the cached sha256, or compute it if necessary.

        If the sha256 value for this charm is not yet cached,
        the compute_sha256() method will be called to compute it.
        """
        if self._sha256 is None:
            self._sha256 = self.compute_sha256()
        return self._sha256
