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

from django.db.models import (OneToOneField, ManyToManyField, Model, CharField,
                              BooleanField)
from django.contrib.auth.models import User
from django.db.models.signals import post_save


User.add_to_class('description', CharField(max_length=160, null=True,
                                           blank=True))
User.add_to_class(
    'location',
    CharField(
        max_length=50,
        null=True,
        blank=True))
User.add_to_class(
    'emailVisible',
    BooleanField(
        default=False))


class UserProfile(Model):
    user = OneToOneField(User, related_name='user_profile')
    follows = ManyToManyField(User, related_name='follows_profile',
                              null=True, blank=True)
    followers = ManyToManyField(User, related_name='followers_profile',
                                null=True, blank=True)

    def __unicode__(self):
        return self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
