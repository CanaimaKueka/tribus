#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie_mongoengine.resources import MongoEngineResource
from tastypie.resources import ModelResource, ALL
from django.contrib.auth.models import User
from tribus.web.models import Trib


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        filtering = {
            'username': ALL,
        }


class TribResource(MongoEngineResource):
    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'tribs'
        authorization = Authorization()
        authentication = SessionAuthentication()
        ordering = ['trib_pub_date']
        filtering = {
            'author_id': ALL,
        }

    def obj_create(self, bundle, **kwargs):
        return super(TribResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)