#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def read_detail(self, object_list, bundle):
        if int(bundle.obj.id) == bundle.request.user.id:
            return True
        raise Unauthorized("You are not allowed to access that resource.")

    def update_detail(self, object_list, bundle):
        if int(bundle.obj.id) == bundle.request.user.id:
            return True
        raise Unauthorized("You are not allowed to access that resource.")


class UserProfileAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id)

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return True

# HACER AUTORIZACION PARA PATCH


    def update_detail(self, object_list, bundle):
        print "details"
        # if int(bundle.obj.id) == bundle.request.user.id:
        return True
        # raise Unauthorized("You are not allowed to access that resource.")

    def delete_list(self, object_list, bundle):
        return object_list

    def delete_detail(self, object_list, bundle):
        return True

class TimelineAuthorization(Authorization):
    def get_timeline(self, bundle):
        follows = bundle.request.user.user_profile.follows.all()
        timeline = [int(f.id) for f in follows]
        timeline.append(bundle.request.user.id)
        return timeline

    def read_list(self, object_list, bundle):
        return object_list.filter(author_id__in=self.get_timeline(bundle=bundle))

    def read_detail(self, object_list, bundle):
        if int(bundle.obj.author_id) in self.get_timeline(bundle=bundle):
            return True
        raise Unauthorized("You are not allowed to access that resource.")


class TribAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        '''
        Everyone can list each other's tribs.
        '''
        return object_list

    def read_detail(self, object_list, bundle):
        '''
        Everyone can read details about each other's tribs.
        '''
        return True

    def create_detail(self, object_list, bundle):
        if int(bundle.obj.author_id) == int(bundle.request.user.id):
            return True
        raise Unauthorized("You are not allowed to access that resource.")

    def delete_list(self, object_list, bundle):
        return EmptyQuerySet()

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("You are not allowed to access that resource.")

class CommentAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return True

    def update_list(self, object_list, bundle):
        return object_list

    def update_detail(self, object_list, bundle):
        return True

    def delete_list(self, object_list, bundle):
        return object_list

    def delete_detail(self, object_list, bundle):
        return True

