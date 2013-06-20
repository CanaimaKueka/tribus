from django.contrib.auth.hashers import BasePasswordHasher

class DummyPasswordHasher(BasePasswordHasher):
    algorithm = "dummy"

    def encode(self, password, salt, iterations=None):
        return password
