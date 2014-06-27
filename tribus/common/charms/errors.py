from tribus.common.errors import CharmError, TribusError


class CharmNotFound(TribusError):
    """A charm was not found in the repository."""

    # This isn't semantically an error with a charm error, its an error
    # even finding the charm.

    def __init__(self, repository_path, charm_name):
        self.repository_path = repository_path
        self.charm_name = charm_name

    def __str__(self):
        return "Charm '%s' not found in repository %s" % (
            self.charm_name, self.repository_path)


class CharmURLError(CharmError):

    def __init__(self, url, message):
        self.url = url
        self.message = message

    def __str__(self):
        return "Bad charm URL %r: %s" % (self.url, self.message)


class MetaDataError(CharmError):
    """Raised when an error in the info file of a charm is found."""

    def __init__(self, *args):
        super(CharmError, self).__init__(*args)

    def __str__(self):
        return super(CharmError, self).__str__()


class InvalidCharmHook(CharmError):
    """A named hook was not found to be valid for the charm."""

    def __init__(self, charm_name, hook_name):
        self.charm_name = charm_name
        self.hook_name = hook_name

    def __str__(self):
        return "Charm %r does not contain hook %r" % (
            self.charm_name, self.hook_name)


class InvalidCharmFile(CharmError):
    """An invalid file was found in a charm."""

    def __init__(self, charm_name, file_path, msg):
        self.charm_name = charm_name
        self.file_path = file_path
        self.msg = msg

    def __str__(self):
        return "Charm %r invalid file %r %s" % (
            self.charm_name, self.file_path, self.msg)


class NewerCharmNotFound(CharmError):
    """A newer charm was not found."""

    def __init__(self, charm_id):
        self.charm_id = charm_id

    def __str__(self):
        return "Charm %r is the latest revision known" % self.charm_id


class ServiceConfigError(CharmError):
    """Indicates an issue related to definition of service options."""


class ServiceConfigValueError(TribusError):
    """Indicates an issue related to values of service options."""


class RepositoryNotFound(TribusError):
    """Indicates inability to locate an appropriate repository"""

    def __init__(self, specifier):
        self.specifier = specifier

    def __str__(self):
        if self.specifier is None:
            return "No repository specified"
        return "No repository found at %r" % self.specifier
