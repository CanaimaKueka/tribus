#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
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

from registration.models import RegistrationManager as BaseRegistrationManager
from registration.models import RegistrationProfile as BaseRegistrationProfile

from django.contrib.auth.models import User
from django.db import transaction


class TribusRegistrationManager(BaseRegistrationManager):
    def create_inactive_user(self, username, last_name, first_name, email,
                             password, site, send_email=True):
        new_user = User.objects.create_user(username, email, password)
        new_user.last_name = last_name
        new_user.first_name = first_name
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user)

        if send_email:
            registration_profile.send_activation_email(site)

        return new_user
    create_inactive_user = transaction.commit_on_success(create_inactive_user)


class TribusRegistrationProfile(BaseRegistrationProfile):
    objects = TribusRegistrationManager()
