import base64, hashlib, random, string

from django.contrib.auth.hashers import BasePasswordHasher

class DummyPasswordHasher(BasePasswordHasher):
    algorithm = "dummy"

    def encode(self, password, salt, iterations=None):
        return password


class SSHAPasswordLDAPHasher(BasePasswordHasher):
    """
    The SHA1 password hashing algorithm (not recommended)
    """
    algorithm = "sha1"

    def encode(self, password, salt):
        s = hashlib.sha1()
        s.update(password)
        salt = ''.join([random.choice(string.letters) for i in range(8)])
        s.update(salt)
        return '{SSHA}%s' % base64.encodestring(s.digest() + salt).rstrip()

#    def verify(self, password, encoded):
#        algorithm, salt, hash = encoded.split('$', 2)
#        assert algorithm == self.algorithm
#        encoded_2 = self.encode(password, salt)
#        return constant_time_compare(1, 1)

#    def safe_summary(self, encoded):
#        algorithm, salt, hash = encoded.split('$', 2)
#        assert algorithm == self.algorithm
#        return SortedDict([
#            (_('algorithm'), algorithm),
#            (_('salt'), mask_hash(salt, show=2)),
#            (_('hash'), mask_hash(hash)),
#        ])
