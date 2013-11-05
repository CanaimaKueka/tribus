#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tastypie.cache import NoCache
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.validation import FormValidation
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.bundle import Bundle
from tastypie import fields
from tastypie_mongoengine.resources import MongoEngineResource


from tastypie.resources import ModelResource, Resource
from tastypie.fields import ManyToManyField, OneToOneField
from tribus.web.api.authorization import (TimelineAuthorization, TribAuthorization, CommentAuthorization, UserAuthorization, UserProfileAuthorization)
from tribus.web.documents import Trib, Comment

from django.contrib.auth.models import User
from tribus.web.profile.models import UserProfile

from haystack.query import SearchQuerySet
from tribus.web.cloud.models import Package


from tribus.web.forms import TribForm


class UserResource(ModelResource):
    user_profile = OneToOneField(to='tribus.web.api.resources.UserProfileResource', attribute='user_profile', related_name='user')

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user/details'
        ordering = ['id']
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get', 'patch']
        filtering = { 'id': ALL_WITH_RELATIONS }
        authorization = UserAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


class UserProfileResource(ModelResource):
    user = OneToOneField(to='tribus.web.api.resources.UserResource', attribute='user', related_name='user_profile')
    follows = ManyToManyField(to='tribus.web.api.resources.UserResource', attribute='follows', related_name='user_profile', blank=True, null=True)
    followers = ManyToManyField(to='tribus.web.api.resources.UserResource', attribute='followers', related_name='user_profile', blank=True, null=True)

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user/profile'
        ordering = ['id']
        allowed_methods = ['get', 'patch']
        filtering = { 'id': ALL_WITH_RELATIONS }
        authorization = UserProfileAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


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
        resource_name = 'user/tribs'
        ordering = ['trib_pub_date']
        allowed_methods = ['get', 'post', 'delete']
        filtering = { 'author_id': ALL_WITH_RELATIONS }
        authorization = TribAuthorization()
        authentication = SessionAuthentication()
        validation = FormValidation(form_class=TribForm)
        cache = NoCache()


class CommentResource(MongoEngineResource):
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'tribs/comments'
        ordering = ['comment_pub_date']
        allowed_methods = ['get', 'post', 'delete']
        filtering = { 'trib_id': ALL_WITH_RELATIONS }
        authorization = CommentAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


class SearchResource(Resource):
    type = fields.CharField(attribute='model_name')
    autoname = fields.CharField(attribute='autoname')
    username = fields.CharField(attribute='username', null=True)
    description = fields.CharField(attribute='description', null=True)
    
    class Meta:
        resource_name = 'search'
        object_class = SearchQuerySet
        authorization = Authorization()
        authentication = SessionAuthentication()
        limit = 10
                 
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.pk
        else:
            kwargs['pk'] = bundle_or_obj.obj.pk
  
        return kwargs
 
    def obj_get_list(self, bundle, **kwargs):
        filters = {}
        if hasattr(bundle.request, 'GET'):
            # Grab a mutable copy.
            filters = bundle.request.GET.copy()
        filters.update(kwargs)
        if filters.has_key('q'):
            sqs = SearchQuerySet().models(Package, User).autocomplete(autoname = filters['q'])
        else:
            sqs = SearchQuerySet().models(Package, User)
        return sqs
