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


from django.db.models.query import EmptyQuerySet
from tastypie.exceptions import Unauthorized
from tastypie.authorization import Authorization as BaseAuthorization


class Authorization(BaseAuthorization):

    def read_list(self, object_list, bundle):
        return EmptyQuerySet()

    def read_detail(self, object_list, bundle):
        raise Unauthorized("You are not allowed to access that resource.")

    def create_list(self, object_list, bundle):
        return EmptyQuerySet()

    def create_detail(self, object_list, bundle):
        raise Unauthorized("You are not allowed to access that resource.")

    def update_list(self, object_list, bundle):
        return EmptyQuerySet()

    def update_detail(self, object_list, bundle):
        raise Unauthorized("You are not allowed to access that resource.")

    def delete_list(self, object_list, bundle):
        return EmptyQuerySet()

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("You are not allowed to access that resource.")


class UserAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id)

    # SE DEBE PERMITIR LEER
    def read_detail(self, object_list, bundle):
        # if int(bundle.obj.id) == bundle.request.user.id:
        return True
        # raise Unauthorized("You are not allowed to access that resource.")

    def update_detail(self, object_list, bundle):
        if int(bundle.obj.id) == bundle.request.user.id:
            return True
        raise Unauthorized("You are not allowed to access that resource.")


class UserProfileAuthorization(Authorization):
    # filtrar todos los objetos pertenecientes a user
    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):  # aqui se debe hacer una val
        return True

# HACER AUTORIZACION PARA PATCH

    def update_detail(self, object_list, bundle):
        # if int(bundle.obj.id) == bundle.request.user.id:
        return True
        # raise Unauthorized("You are not allowed to access that resource.")


class UserFollowersAuthorization(Authorization):

    def get_followers(self, bundle):
        search = bundle.request.user.user_profile.followers.all()
        followers = [int(f.id) for f in search]
        return followers

    def read_list(self, object_list, bundle):
        return object_list.filter(id__in=self.get_followers(bundle=bundle))


class UserFollowsAuthorization(Authorization):

    def get_follows(self, bundle):
        search = bundle.request.user.user_profile.follows.all()
        follows = [int(f.id) for f in search]
        return follows

    def read_list(self, object_list, bundle):
        return object_list.filter(id__in=self.get_follows(bundle=bundle))


class TimelineAuthorization(Authorization):

    def get_timeline(self, bundle):
        follows = bundle.request.user.user_profile.follows.all()
        timeline = [int(f.id) for f in follows]
        timeline.append(bundle.request.user.id)

        return timeline

    def read_list(self, object_list, bundle):
        return object_list.filter(user_id__in=self.get_timeline(bundle=bundle))

    def read_detail(self, object_list, bundle):
        if int(bundle.obj.user_id) in self.get_timeline(bundle=bundle):
            return True
        raise Unauthorized("You are not allowed to access that resource.")


class TribAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        """
        Everyone can list each other's tribs.
        """
        return object_list

    def read_detail(self, object_list, bundle):
        """
        Everyone can read details about each other's tribs.
        """
        return True

    def create_detail(self, object_list, bundle):
        if not bundle.request.user.is_anonymous():
            if int(bundle.obj.user_id.id) == int(bundle.request.user.id):
                return True
        raise Unauthorized("You are not allowed to access that resource.")

    def delete_detail(self, object_list, bundle):
        if not bundle.request.user.is_anonymous():
            if int(bundle.obj.user_id.id) == int(bundle.request.user.id):
                return True
        raise Unauthorized("You are not allowed to access that resource.")


class CommentAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def create_detail(self, object_list, bundle):
        if not bundle.request.user.is_anonymous():
            if int(bundle.obj.user_id.id) == int(bundle.request.user.id):
                return True
        raise Unauthorized("You are not allowed to access that resource.")

    def delete_detail(self, object_list, bundle):
        if not bundle.request.user.is_anonymous():
            if int(bundle.obj.user_id.id) == int(bundle.request.user.id):
                return True
        raise Unauthorized("You are not allowed to access that resource.")
