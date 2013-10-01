#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication, Authentication
from tastypie_mongoengine.resources import MongoEngineResource
from tastypie.resources import ModelResource, ALL
from django.contrib.auth.models import User
from tribus.web.models import Trib


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        filtering = {
            'username': ALL,
        }


class TribResource(MongoEngineResource):
    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'user/tribs'
        authorization = Authorization()
        authentication = SessionAuthentication()
        ordering = ['trib_pub_date']
        filtering = {
            'author_id': ALL,
        }

    def obj_create(self, bundle, **kwargs):
        return super(TribResource, self).obj_create(bundle, author_id=bundle.request.user.id)

    def apply_authorization_limits(self, request, object_list):
        print object_list
        return object_list.filter(author_id=request.user.id)


class TimelineResource(MongoEngineResource):
    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'user/timeline'
        authorization = Authorization()
        authentication = SessionAuthentication()
        ordering = ['trib_pub_date']
        filtering = {
            'author_id': ALL,
            'author_username': ALL,
        }

    def get_object_list(self, request):
        
        user_profile = User.objects.get(user_id__id__exact=request.user.id)
        user_timeline = [u.id for u in User.follows.all()]
        user_timeline.append(request.user.id)

        return super(TimelineResource, self).get_object_list(request).filter(author_id__in=user_timeline)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(author_id=request.user.id)