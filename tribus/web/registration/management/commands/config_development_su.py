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

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from tribus.web.registration.ldap.utils import create_ldap_user


class Command(BaseCommand):

    def handle(self, *args, **options):

        try:
            u = User.objects.get(username__exact='tribus')
        except User.DoesNotExist:
            u = User(username='tribus')
            u.set_password('tribus')
            u.is_superuser = True
            u.is_staff = True
            u.save()
            create_ldap_user(u)
