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


from tastypie.cache import NoCache
from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import fields
from tastypie_mongoengine.resources import MongoEngineResource

from tastypie.resources import ModelResource, Resource
from tastypie.fields import ManyToManyField, OneToOneField
from tribus.web.api.authorization import (TimelineAuthorization, TribAuthorization, CommentAuthorization, UserAuthorization, UserProfileAuthorization)
from tribus.web.documents import Trib, Comment

from django.contrib.auth.models import User
from tribus.web.profile.models import UserProfile

from haystack.query import SearchQuerySet, EmptySearchQuerySet
from tribus.web.cloud.models import Package


from tribus.web.api.validation import DocumentFormValidation
from tribus.web.forms import TribForm
from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from django.http.response import Http404


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
        validation = DocumentFormValidation(form_class=TribForm)
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


class SearchUserResource(Resource):
    name = fields.CharField(attribute='autoname')
    description = fields.CharField(attribute='description')
    
    class Meta:
        resource_name = 'search'
        object_class = User
    
    def obj_get_list(self, bundle, **kwargs):
        filters = {}
        if hasattr(bundle.request, 'GET'):
            filters = bundle.request.GET.copy()
        filters.update(kwargs)
        if filters.has_key('q'):
            sqs = SearchQuerySet().models(User).autocomplete(autoname = filters['q'])[:5]
        else:
            sqs = EmptySearchQuerySet()
            
        paginator = Paginator(filter(None, sqs), 5)
        
        try:
            page = paginator.page(1)
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        return page
    
class SearchPackageResource(Resource):
    name = fields.CharField(attribute='autoname')
    description = fields.CharField(attribute='description')
    
    class Meta:
        resource_name = 'search'
        object_class = Package
    
    def obj_get_list(self, bundle, **kwargs):
        filters = {}
        if hasattr(bundle.request, 'GET'):
            filters = bundle.request.GET.copy()
        filters.update(kwargs)
        if filters.has_key('q'):
            sqs = SearchQuerySet().models(Package).autocomplete(autoname = filters['q'])[:5]
        else:
            sqs = EmptySearchQuerySet()
        
        paginator = Paginator(filter(None, sqs), 5)
        
        try:
            page = paginator.page(int(bundle.request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        return page

class SearchResource(Resource):
    users = fields.ListField()
    packages = fields.ListField()
    
    class Meta:
        resource_name = 'search'
        allowed_methods = ['get']
        include_resource_uri = False

    def dehydrate_users(self, bundle):
        return [ {'fullname':str(obj.fullname), 'username': str(obj.username)} for obj in bundle.obj['users']]
    
    def dehydrate_packages(self, bundle):
        return [ {'name':str(obj.name)} for obj in bundle.obj['packages']]

    def get_object_list(self, bundle):
        return [{'users': SearchUserResource().obj_get_list(bundle),
                 'packages': SearchPackageResource().obj_get_list(bundle),}]
                
    def obj_get_list(self, bundle, **kwargs): 
        return self.get_object_list(bundle)    
