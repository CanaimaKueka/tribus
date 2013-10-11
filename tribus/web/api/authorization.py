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


class TimelineAuthorization(Authorization):
    def get_timeline(self, bundle):
        follows = bundle.request.user.follows.all()
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
        return object_list.filter(author_id__exact=int(bundle.request.user.id))

    def read_detail(self, object_list, bundle):
        if int(bundle.obj.author_id) == int(bundle.request.user.id):
            return True
        raise Unauthorized("You are not allowed to access that resource.")

    def create_detail(self, object_list, bundle):
        if int(bundle.obj.author_id) == int(bundle.request.user.id):
            return True
        raise Unauthorized("You are not allowed to access that resource.")

    def delete_list(self, object_list, bundle):
        return EmptyQuerySet()

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("You are not allowed to access that resource.")

