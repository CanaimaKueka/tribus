#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import base64
import hashlib
import random
import string

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

    def encode(self, password, salt, iterations=None):
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
