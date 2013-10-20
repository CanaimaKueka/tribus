#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from tastypie.cache import NoCache
from tastypie.authentication import SessionAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.bundle import Bundle
from tastypie_mongoengine.resources import MongoEngineResource

from tastypie.resources import ModelResource
from tastypie.fields import ManyToManyField, OneToOneField
from tribus.web.api.authorization import (TimelineAuthorization, TribAuthorization, CommentAuthorization, UserAuthorization)
from tribus.web.documents import Trib, Comment

from tastypie_mongoengine.fields import EmbeddedListField
from django.contrib.auth.models import User
from tribus.web.profile.models import UserProfile


class UserResource(ModelResource):
    user_profile = OneToOneField(to='tribus.web.api.resources.UserProfileResource', attribute='user_profile', related_name='user')

    class Meta:
        queryset = User.objects.all()
        resource_name = 'details'
        detail_uri_name = 'id'
        ordering = ['id']
        allowed_methods = ['get', 'patch']
        hierarchy = 'username'
        filtering = { 'username': ALL_WITH_RELATIONS }
        authorization = Authorization()
        authentication = Authentication()
        cache = NoCache()        

    def base_urls(self):
        return [
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)$' %
                (self._meta.hierarchy, self._meta.resource_name),
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)/schema$' %
                (self._meta.hierarchy, self._meta.resource_name),
                self.wrap_view('get_schema'), name="api_get_schema"),
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)/set/(?P<%s_list>\w[\w/;-]*)$' %
                (self._meta.hierarchy, self._meta.resource_name, self._meta.detail_uri_name),
                self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)/(?P<%s>\w[\w/-]*)$' %
                (self._meta.hierarchy, self._meta.resource_name, self._meta.detail_uri_name),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def resource_uri_kwargs(self, bundle_or_obj=None):
        kwargs = super(UserResource, self).resource_uri_kwargs(bundle_or_obj)

        if bundle_or_obj is not None:
            try:
                if isinstance(bundle_or_obj, Bundle):
                    kwargs[self._meta.hierarchy] = getattr(bundle_or_obj.obj, self._meta.hierarchy)
                else:
                    kwargs[self._meta.hierarchy] = getattr(bundle_or_obj, self._meta.hierarchy)
            except Exception, e:
                print e
        return kwargs


class UserProfileResource(ModelResource):
    user = OneToOneField(to='tribus.web.api.resources.UserResource', attribute='user', related_name='user_profile')
    follows = ManyToManyField(to='tribus.web.api.resources.UserResource', attribute='follows_profile', related_name='user_profile', blank=True, null=True)
    followers = ManyToManyField(to='tribus.web.api.resources.UserResource', attribute='followers_profile', related_name='user_profile', blank=True, null=True)

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'profile'
        detail_uri_name = 'id'
        ordering = ['id']
        allowed_methods = ['get', 'patch']
        hierarchy = 'user'
        filtering = { 'user': ALL_WITH_RELATIONS }
        authorization = Authorization()
        authentication = Authentication()
        cache = NoCache()        

    def base_urls(self):
        return [
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)$' %
                (self._meta.hierarchy, self._meta.resource_name),
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)/schema$' %
                (self._meta.hierarchy, self._meta.resource_name),
                self.wrap_view('get_schema'), name="api_get_schema"),
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)/set/(?P<%s_list>\w[\w/;-]*)$' %
                (self._meta.hierarchy, self._meta.resource_name, self._meta.detail_uri_name),
                self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)/(?P<%s>\w[\w/-]*)$' %
                (self._meta.hierarchy, self._meta.resource_name, self._meta.detail_uri_name),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def resource_uri_kwargs(self, bundle_or_obj=None):
        kwargs = super(UserProfileResource, self).resource_uri_kwargs(bundle_or_obj)

        if bundle_or_obj is not None:
            try:
                if isinstance(bundle_or_obj, Bundle):
                    kwargs[self._meta.hierarchy] = getattr(bundle_or_obj.obj, self._meta.hierarchy)
                else:
                    kwargs[self._meta.hierarchy] = getattr(bundle_or_obj, self._meta.hierarchy)
            except Exception, e:
                print e
        return kwargs


class TimelineResource(MongoEngineResource):
    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'user/timeline'
        ordering = ['trib_pub_date']
        allowed_methods = ['get']
        authorization = TimelineAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


class TribResource(MongoEngineResource):
    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'tribs'
        detail_uri_name = 'id'
        ordering = ['trib_pub_date']
        allowed_methods = ['get', 'post', 'delete']
        hierarchy = 'author_username'
        filtering = { 'author_username': ALL_WITH_RELATIONS }
        authorization = TribAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()

    def base_urls(self):
        return [
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)$' %
                (self._meta.hierarchy, self._meta.resource_name),
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)/schema$' %
                (self._meta.hierarchy, self._meta.resource_name),
                self.wrap_view('get_schema'), name="api_get_schema"),
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)/set/(?P<%s_list>\w[\w/;-]*)$' %
                (self._meta.hierarchy, self._meta.resource_name, self._meta.detail_uri_name),
                self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r'^(?P<%s>[\w\d_.-]+)/(?P<resource_name>%s)/(?P<%s>\w[\w/-]*)$' %
                (self._meta.hierarchy, self._meta.resource_name, self._meta.detail_uri_name),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def resource_uri_kwargs(self, bundle_or_obj=None):
        kwargs = super(TribResource, self).resource_uri_kwargs(bundle_or_obj)

        if bundle_or_obj is not None:
            try:
                if isinstance(bundle_or_obj, Bundle):
                    kwargs[self._meta.hierarchy] = getattr(bundle_or_obj.obj, self._meta.hierarchy)
                else:
                    kwargs[self._meta.hierarchy] = getattr(bundle_or_obj, self._meta.hierarchy)
            except Exception, e:
                print e
        return kwargs


class CommentResource(MongoEngineResource):
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comments'
        detail_uri_name = 'id'
        ordering = ['comment_pub_date']
        allowed_methods = ['get', 'post', 'delete']
        hierarchy = 'trib_id'
        filtering = { 'trib_id': ALL_WITH_RELATIONS }
        authorization = CommentAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()

    def base_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/(?P<%s>[\w\d_.-]+)$' %
                (self._meta.resource_name, self._meta.hierarchy),
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r'^(?P<resource_name>%s)/(?P<%s>[\w\d_.-]+)/schema$' %
                (self._meta.resource_name, self._meta.hierarchy),
                self.wrap_view('get_schema'), name="api_get_schema"),
            url(r'^(?P<resource_name>%s)/(?P<%s>[\w\d_.-]+)/set/(?P<%s_list>\w[\w/;-]*)$' %
                (self._meta.resource_name, self._meta.hierarchy, self._meta.detail_uri_name),
                self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r'^(?P<resource_name>%s)/(?P<%s>[\w\d_.-]+)/(?P<%s>\w[\w/-]*)$' %
                (self._meta.resource_name, self._meta.hierarchy, self._meta.detail_uri_name),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def resource_uri_kwargs(self, bundle_or_obj=None):
        kwargs = super(CommentResource, self).resource_uri_kwargs(bundle_or_obj)

        if bundle_or_obj is not None:
            try:
                if isinstance(bundle_or_obj, Bundle):
                    kwargs[self._meta.hierarchy] = getattr(bundle_or_obj.obj, self._meta.hierarchy)
                else:
                    kwargs[self._meta.hierarchy] = getattr(bundle_or_obj, self._meta.hierarchy)
            except Exception, e:
                print e
        return kwargs


        '''
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"author_id": 2, "author_username": "luis", "author_first_name": "Luis Alejandro", "author_last_name": "Martínez Faneyth", "author_email": "luis@huntingbears.com.ve", "comment_content": "hola", "comment_pub_date": "2013-09-25T00:03:55.804000", "trib_id": "525b5e4fea10251d9969b97e"}' http://localhost:8000/api/0.1/comments/525b5e4fea10251d9969b97e
        '''
